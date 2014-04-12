from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from querystring_parser import parser

from decimal import Decimal
from datetime import datetime
import urllib
import json
import uuid

from shop.models import Item, DeliveryOption
from order.models import Invoice, Coupon, Order, OrderItem, DeliveryWindow, Payment
from order.forms import CheckoutForm
from order import paypal

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

def validate_delivery_choices(delivery_choices):
    options = {}
    for (store_slug, option_id) in delivery_choices.items():
      option = DeliveryOption.objects.get(id=option_id)
      if option.store.slug != store_slug or not option.in_effect:
        return False
      options[option.store] = option
    return options

# Views

def view_cart(request):

  # Get cart
  cart = cart_from_request(request)
  error = None

  # If is a submit, pre validate the data
  if request.method == 'POST' and isinstance(cart, list) and len(cart) > 0:

    # Get cart options
    post = parser.parse(request.POST.urlencode())

    coupon_code = post.get('coupon_code')
    coupon = Coupon.objects.get_valid_coupon(coupon_code)

    page_datetime = datetime.fromtimestamp(post.get('datetime'))
    allow_sub_detail = post.get('allow_sub_detail')
    allow_sub_detail = {} if allow_sub_detail is None else allow_sub_detail

    # Validate delivery choices
    delivery_choices = post.get('delivery_choices')
    delivery_options = validate_delivery_choices(delivery_choices)

    if delivery_options == False:
      error = 'The delivery option you select is no longer valid'
    elif len(coupon_code) > 0 and coupon == False:
      error = 'The coupon you have entered is no longer valid'
    else:
      request.session['checkout_package'] = {
        'cart': cart,
        'delivery_choices': delivery_choices,
        'allow_sub_detail': allow_sub_detail,
        'coupon_code': coupon_code,
        'page_datetime': page_datetime,
      }
      response = HttpResponseRedirect(reverse('order:checkout'))
      return response

  store_items = cart_to_store_items(cart)
  template = loader.get_template('order/cart.html')
  context = RequestContext(request, {
    'store_items': store_items,
    'datetime': datetime.now(),
    'error': error,
  })
  return HttpResponse(template.render(context))

def checkout(request):
  error = None
  try:
     checkout_package = request.session['checkout_package']
     if checkout_package is None or len(checkout_package) <= 0:
         return HttpResponseRedirect(reverse('order:cart'))
  except KeyError:
      return HttpResponseRedirect(reverse('order:cart'))


  cart = checkout_package['cart'];
  delivery_choices = checkout_package['delivery_choices'];
  allow_sub_detail = checkout_package['allow_sub_detail'];
  coupon_code = checkout_package['coupon_code'];
  page_datetime = checkout_package['page_datetime'];

  store_items = cart_to_store_items(cart)
  coupon = Coupon.objects.get_valid_coupon(coupon_code)
  delivery_options = validate_delivery_choices(delivery_choices)

  if request.method == 'POST' and isinstance(cart, list) and len(cart) > 0:
    # No response by default
    response = None
    checkout_form = CheckoutForm(request.POST)

    if delivery_options == False:
      error = 'The delivery option you select is no longer valid'
      return HttpResponseRedirect(reverse('order:cart'))
    elif len(coupon_code) > 0 and coupon == False:
      error = 'The coupon you have entered is no longer valid'
      return HttpResponseRedirect(reverse('order:cart'))
    elif checkout_form.is_valid():
      payment_method = checkout_form.cleaned_data['payment_method']
      user = None
      if request.user and request.user.is_authenticated():
         user = request.user
      invoice = create_invoice(
        store_items,
        checkout_form,
        delivery_options,
        allow_sub_detail,
        page_datetime,
        coupon,
        user
      )

      # If is not paypal, create payment directly
      if payment_method != Payment.METHODS_PAYPAL:
        Payment.objects.create_payment(invoice, payment_method)
        invoice.set_status(Invoice.STATUS_PAY_ON_DELIVERY)
        response = HttpResponseRedirect(reverse('order:show', kwargs={'id': invoice.id}))
        response.set_cookie('cart', '')
      else:
        raw_payment = paypal.create_raw_payment_for_invoice(invoice, {
          'return_url': request.build_absolute_uri(reverse('order:payment_paypal_execute', kwargs={'id': invoice.id})),
          'cancel_url': request.build_absolute_uri(reverse('order:payment_paypal_cancel', kwargs={'id': invoice.id})),
        })
        if raw_payment is None:
          error = 'Fail to create the PayPal payment at the moment, please try again or choose another payment method'
        else:
          payment = Payment.objects.create_paypal_payment(invoice, raw_payment)
          redirect_url = paypal.get_redirect_url(payment.raw, reverse('shop:to_default'))
          response = HttpResponseRedirect(redirect_url)

    if response is not None:
      # Clean up checkout_package
      request.session['checkout_package'] = None
      return response

  else:
    checkout_form = CheckoutForm();

  template = loader.get_template('order/checkout.html')
  context = RequestContext(request, {
    'store_items': store_items,
    'delivery_options': delivery_options,
    'allow_sub_detail': allow_sub_detail,
    'datetime': datetime.now(),
    'coupon_code': coupon_code,
    'checkout_form': checkout_form,
    'error': error,
  })
  return HttpResponse(template.render(context))

def show_invoice(request, id):
  template_name = 'order/show.html'

  return render(request, template_name, { 'id': id })

def show_invoice_num(request, invoice_num):
  template = loader.get_template('order/invoice.html')
  try:
    invoice = Invoice.objects.get(invoice_num=invoice_num)
  except ObjectDoesNotExist:
    return HttpResponse('Invalid invoice number', status=404)

  # Check access permission
  if invoice.user:
    if not request.user.is_authenticated():
      return HttpResponseRedirect(reverse('django.contrib.auth.views.login') + '?next=' + request.path)
    if invoice.user.id != request.user.id and request.user.groups.filter(name='driver').count() == 0:
      return HttpResponseRedirect(reverse('shop:to_default'))

  # Setup context and render
  context = RequestContext(request, {
    'invoice': invoice,
  })

  return HttpResponse(template.render(context))

# PayPal

def payment_paypal_execute(request, id):
  id = int(id)
  try:
    invoice = Invoice.objects.get(id=id)
  except ObjectDoesNotExist:
    return HttpResponse('Invalid invoice id', status=404)
  payer_id = request.GET['PayerID']
  payments = invoice.payments.all()
  for payment in payments:
    if payment.status == Payment.STATUS_COMPLETED:
      continue
    raw_payment = paypal.execute_payment(payment.raw, payer_id)
    if raw_payment is not None:
      payment.raw = json.dumps(raw_payment.to_dict())
      payment.set_status(Payment.STATUS_COMPLETED)
      # Clear cookie cart and redirect to show the order.
      response = HttpResponseRedirect(reverse('order:show', kwargs={'id': invoice.id}))
      response.set_cookie('cart', '')
      return response
  return HttpResponse('Failed to execute your payment. Please contact us for help.')

def payment_paypal_cancel(request, id):
  id = int(id)
  try:
    invoice = Invoice.objects.get(id=id)
  except ObjectDoesNotExist:
    return HttpResponse('Invalid invoice id', status=404)
  if invoice.status == Invoice.STATUS_PENDING:
    payments = invoice.payments.all()
    for payment in payments:
      payment.set_status(Payment.STATUS_CANCELLED)
  return HttpResponseRedirect(reverse('order:show', kwargs={'id': invoice.id}))

# API

def coupon(request, code):
  coupon = Coupon.objects.get_valid_coupon(code)
  if coupon is False:
    return empty_response()
  return json_response([coupon])

# Invoice and Order process

def create_invoice(store_items, checkout_form, delivery_options, allow_sub_detail, page_datetime, coupon, user):
  # Gether info from POST to setup the order
  # Customer infos
  customer_name = checkout_form.cleaned_data['name']
  address = checkout_form.cleaned_data['address']
  postcode = checkout_form.cleaned_data['postcode']
  phone = checkout_form.cleaned_data['phone']
  email = checkout_form.cleaned_data['email']
  comment = checkout_form.cleaned_data['comment']

  # Invoice infos
  invoice_num = str(uuid.uuid4())
  delivery = Decimal('0.99')
  discount = Decimal(0)

  # Apply coupon
  if isinstance(coupon, Coupon):
    discount = coupon.value
    coupon.used = True;
    # TODO: handle percentage coupon
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
    delivery = delivery,
    discount = discount,

    # Customer
    customer_name = customer_name,
    address = address,
    postcode = postcode,
    phone = phone,
    email = email,
    user = user
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
      comment = comment,

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
      quantity = wrap['quantity']
      quantity = item.max_quantity_per_order if item.max_quantity_per_order > 0 and quantity > item.max_quantity_per_order else quantity
      if quantity <= 0:
        continue

      allow_sub = allow_sub_detail.get(item.id) == "on"
      unit_price = item.sales_price if item.on_sale else item.price
      item_cost = (unit_price * quantity).quantize(Decimal('.01'))
      item_tax = (item_cost * item.tax_class).quantize(Decimal('.01'))

      OrderItem.objects.create(
        order = order,
        item = item,
        quantity = quantity,
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

  if coupon is not None:
    coupon.save()

  return invoice
