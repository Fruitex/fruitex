from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.core import serializers
from django.core.urlresolvers import reverse
from django.conf import settings

from paypal.standard.forms import PayPalPaymentsForm
from querystring_parser import parser

from datetime import date
from decimal import Decimal
import urllib
import json
import uuid

from shop.models import Item, DeliveryOption
from order.models import Order, OrderItem, Invoice, Coupon, DeliveryWindow

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
  template = loader.get_template('order/cart.html')

  cart = cart_from_request(request)
  store_items = cart_to_store_items(cart)

  context = RequestContext(request, {
    'store_items': store_items,
  })
  return HttpResponse(template.render(context))

@csrf_exempt
def show_invoice(request, id):
  template = loader.get_template('order/show.html')

  invoice = Invoice.objects.get(id=id)

  # Setup context and render
  context = Context({
    'invoice': invoice,
  })
  return HttpResponse(template.render(context))

def new_from_cart(request):
  template = loader.get_template('order/show.html')

  post = parser.parse(request.POST.urlencode())
  # return HttpResponse(json.dumps(post))

  # Gether info from POST to setup the order
  # Customer infos
  customer_name = str(post['name'])
  address = str(post['address'])
  postcode = str(post['postcode'])
  phone = str(post['phone'])
  email = str(post['email'])

  # Order infos
  invoice_num = str(uuid.uuid4())
  delivery_options = post['delivery_options']
  coupon_code = str(post['coupon_code'])
  item_ids = json.loads(post['item_ids']);
  allow_sub_detail = post['allow_sub_detail']

  # Validate coupon
  discount = Decimal(0)
  shipping = Decimal(4)

  if coupon_code is not None and len(coupon_code) > 0:
    coupon = Coupon.objects.get_valid_coupon(coupon_code)
    if coupon != False:
      # TODO: handle percentage coupon
      discount = coupon.value
    else:
      coupon = None

  # Create invoice
  invoice = Invoice.objects.create(
    # Infos
    invoice_num = invoice_num,
    status = Invoice.STATUS_PENDING,
    coupon = coupon,

    # Amount
    subtotal = Decimal(0),
    tax = Decimal(0),
    shipping = shipping,
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
    option = DeliveryOption.objects.get(id=delivery_options[store.slug])

    # Create order
    order = Order.objects.create(
      # Order
      subtotal = Decimal(0),
      tax = Decimal(0),
      delivery_window = DeliveryWindow.objects.get_window(option, date.today()),

      # Meta
      invoice = invoice,
      status = Order.STATUS_PENDING,
    )
    orders[store] = order
    return order

  # Fetch items from cart and db
  store_items = cart_to_store_items(item_ids)

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

  # Setup paypal dict
  paypal_dict = {
    "business": settings.PAYPAL_RECEIVER_EMAIL,
    "currency_code": "CAD",
    "amount": "%.2f" % invoice.total,
    "item_name": "Fruitex order #%d" % invoice.id,
    "invoice": invoice_num,
    "notify_url": request.build_absolute_uri(reverse('order:paypal-ipn')),
    "return_url": request.build_absolute_uri(reverse('order:show', kwargs={'id': invoice.id})),
    "cancel_return": request.build_absolute_uri(reverse('shop:to_default')),
    "custom": json.dumps({'coupon': coupon_code})
  }

  # Create the Paypal form
  form = PayPalPaymentsForm(initial=paypal_dict)

  # Setup context and render
  context = Context({
    'invoice': invoice,
    'form': form,
    'sandbox': settings.DEBUG,
  })
  response = HttpResponse(template.render(context))
  response.set_cookie('cart', '')
  return response

# API

def coupon(request, code):
  coupon = Coupon.objects.get_valid_coupon(code)
  if coupon is False:
    return empty_response()
  return json_response([coupon])
