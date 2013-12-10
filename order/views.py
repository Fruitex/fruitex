from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.conf import settings
from django import forms
from django.core.exceptions import ValidationError

from paypal.standard.forms import PayPalPaymentsForm
from querystring_parser import parser

from datetime import date, datetime
from decimal import Decimal
import urllib
import json
import uuid

from shop.models import Item, DeliveryOption
from order.models import Order, OrderItem, Invoice, Coupon, DeliveryWindow

# Checkout form definition

class CheckoutForm(forms.Form):
  def _validate_coupon_code(coupon_code):
    coupon = Coupon.objects.get_valid_coupon(coupon_code)
    if coupon == False:
      raise ValidationError(u'%s is not a valid coupon' % coupon_code)

  name = forms.CharField(max_length=64, validators=[
    RegexValidator(regex=r'^[a-zA-Z ]+$'),
  ])
  phone = forms.CharField(max_length=16, validators=[
    RegexValidator(regex=r'^(\+1){0,1}\({0,1}\d{3}[ -\)]{0,1}\d{3}[ -]{0,1}\d{4}$'),
  ])
  email = forms.EmailField()
  address = forms.CharField(min_length=8)
  postcode = forms.CharField(max_length=8, validators=[
    RegexValidator(regex=r'^[a-zA-Z]\d[a-zA-Z] {0,1}\d[a-zA-Z]\d$'),
  ])
  coupon_code = forms.CharField(required=False, validators=[_validate_coupon_code])

# Common operations

def empty_response():
  return HttpResponse('[]', mimetype='application/json')

def json_response(queryset):
  return HttpResponse(serializers.serialize('json', queryset), mimetype='application/json')

def cart_from_request(request):
  cart = request.COOKIES.get('cart')
  if cart is None or len(cart) == 0:
    return []
  cart = urllib.unquote(cart)
  cart = json.loads(cart)
  return cart

def cart_to_store_items(cart):
  cart_items = Item.objects.filter(id__in=cart)
  json_value = json.loads(serializers.serialize('json', cart_items))

  store_items = {}

  for i, item in enumerate(cart_items):
    store = item.category.store

    if store not in store_items:
      store_items[store] = []

    store_items[store].append({
      'obj': item,
      'quantity': cart.count(item.id),
      'json': json.dumps(json_value[i])
    })

  return store_items

# Views

def view_cart(request):
  def _validate_delivery_choices(delivery_choices):
    options = {}
    for (store_slug, option_id) in delivery_choices.items():
      option = DeliveryOption.objects.get(id=option_id)
      if option.store.slug != store_slug or not option.in_effect:
        return False
      options[option.store] = option
    return options

  # Get store_items
  cart = cart_from_request(request)
  store_items = cart_to_store_items(cart)

  # If is a submit, pre validate the data
  if request.method == 'POST' and isinstance(cart, list) and len(cart) > 0:
    checkout_form = CheckoutForm(request.POST)

    # Validate form
    if checkout_form.is_valid():
      post = parser.parse(request.POST.urlencode())

      # Validate delivery choices
      delivery_choices = post.get('delivery_choices')
      page_datetime = datetime.fromtimestamp(post.get('datetime'))
      delivery_options = _validate_delivery_choices(delivery_choices)

      allow_sub_detail = post.get('allow_sub_detail')
      allow_sub_detail = {} if allow_sub_detail is None else allow_sub_detail

      if delivery_options != False:
        return place_order(store_items, checkout_form, delivery_options,
                           allow_sub_detail, page_datetime)
  else:
    checkout_form = CheckoutForm()

  template = loader.get_template('order/cart.html')
  context = RequestContext(request, {
    'store_items': store_items,
    'datetime': datetime.now(),
    'checkout_form': checkout_form,
  })
  return HttpResponse(template.render(context))

@csrf_exempt
def show_invoice(request, id):
  template = loader.get_template('order/show.html')

  invoice = Invoice.objects.get(id=id)

  if invoice.status == invoice.STATUS_PENDING:
    custom = None if invoice.coupon is None else {'coupon': invoice.coupon.code}

    # Setup paypal dict
    paypal_dict = {
      "business": settings.PAYPAL_RECEIVER_EMAIL,
      "currency_code": "CAD",
      "amount": "%.2f" % invoice.total,
      "item_name": "Fruitex order #%d" % invoice.id,
      "invoice": invoice.invoice_num,
      "notify_url": request.build_absolute_uri(reverse('order:paypal-ipn')),
      "return_url": request.build_absolute_uri(reverse('order:show', kwargs={'id': invoice.id})),
      "cancel_return": request.build_absolute_uri(reverse('shop:to_default')),
      "custom": json.dumps(custom)
    }

    # Create the Paypal form
    form = PayPalPaymentsForm(initial=paypal_dict)
  else:
    form = None

  # Setup context and render
  context = Context({
    'invoice': invoice,
    'form': form,
    'sandbox': settings.DEBUG,
  })

  return HttpResponse(template.render(context))


# API

def coupon(request, code):
  coupon = Coupon.objects.get_valid_coupon(code)
  if coupon is False:
    return empty_response()
  return json_response([coupon])


# Invoice and Order process

def place_order(store_items, checkout_form, delivery_options, allow_sub_detail, page_datetime):
  # Gether info from POST to setup the order
  # Customer infos
  customer_name = checkout_form.cleaned_data['name']
  address = checkout_form.cleaned_data['address']
  postcode = checkout_form.cleaned_data['postcode']
  phone = checkout_form.cleaned_data['phone']
  email = checkout_form.cleaned_data['email']

  # Invoice infos
  invoice_num = str(uuid.uuid4())
  delivery = Decimal(4)
  discount = Decimal(0)
  coupon_code = checkout_form.cleaned_data['coupon_code']

  # Get coupon
  coupon = None
  if coupon_code is not None and len(coupon_code) > 0:
    coupon = Coupon.objects.get_valid_coupon(coupon_code)
    discount = coupon.value
    # TODO: handle percentage coupon

  # Create invoice
  invoice = Invoice.objects.create(
    # Infos
    invoice_num = invoice_num,
    status = Invoice.STATUS_PENDING,
    coupon = coupon,

    # Amount
    subtotal = Decimal(0),
    tax = Decimal(0),
    delivery = delivery,
    discount = discount,

    # Customer
    customer_name = customer_name,
    address = address,
    postcode = postcode,
    phone = phone,
    email = email,
  )

  # Construct orders
  orders = {}
  def get_order_for_store(store):
    if store in orders:
      return orders.get(store_slug)

    # Fetch Delivery Option
    option = delivery_options[store]

    # Create order
    order = Order.objects.create(
      # Order
      subtotal = Decimal(0),
      tax = Decimal(0),
      delivery_window = DeliveryWindow.objects.get_window(option, page_datetime),

      # Meta
      invoice = invoice,
      status = Order.STATUS_PENDING,
    )
    orders[store] = order
    return order

  # Add order items and calculate subtotal and tax
  for (store, items) in store_items.items():
    order = get_order_for_store(store)
    for wrap in items:
      item = wrap['obj']

      allow_sub = allow_sub_detail.get(item.id) == "on"
      unit_price = item.sales_price if item.on_sale else item.price
      item_cost = unit_price * wrap['quantity']
      item_tax = item_cost * item.tax_class

      OrderItem.objects.create(
        order = order,
        item = item,
        quantity = wrap['quantity'],
        allow_sub = allow_sub,
        item_cost = item_cost,
        item_tax = item_tax,
      )

      # Update subtotal and tax
      order.subtotal += item_cost
      order.tax += item_tax

  # Save orders and invoice
  for (store_slug, order) in orders.items():
    invoice.subtotal += order.subtotal;
    invoice.tax += order.tax;
    order.save()
  invoice.save()

  response = HttpResponseRedirect(reverse('order:show', kwargs={'id': invoice.id}))
  response.set_cookie('cart', '')

  return response
