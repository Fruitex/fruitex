from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.core import serializers
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm

from datetime import datetime
from datetime import timedelta
from decimal import Decimal
import urllib
import json
import uuid

from shop.models import Item
from order.models import Order, OrderItem, Invoice
from config.paypal import PAYPAL_RECEIVER_EMAIL
from config.environment import DEBUG

# Common operations

def cart_from_request(request):
  cart = request.COOKIES.get('cart')
  if cart is None or len(cart) == 0:
    return []
  cart = urllib.unquote(cart)
  cart = json.loads(cart)
  return cart

def cart_items(cart):
  items = Item.objects.filter(id__in=cart)
  json_value = serializers.serialize('json', items)
  json_value = json.loads(json_value)
  return [{
    'obj': item,
    'quantity': cart.count(item.id),
    'json': json.dumps(json_value[i])
  } for i, item in enumerate(items)]

# Views

def view_cart(request):
  template = loader.get_template('order/cart.html')

  cart = cart_from_request(request)
  items = cart_items(cart)
  today = datetime.now()
  tomorrow = today + timedelta(days=1)

  context = RequestContext(request, {
    'items': items,
    'today': today,
    'tomorrow': tomorrow,
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

  # Gether info from POST to setup the order
  # Customer infos
  customer_name = request.POST['name']
  address = request.POST['address']
  postcode = request.POST['postcode']
  phone = request.POST['phone']
  email = request.POST['email']

  # Order infos
  invoice_num = str(uuid.uuid4())
  delivery_window = request.POST['time']
  coupon_code = request.POST['coupon']

  # Validate coupon
  # TODO
  coupon = None
  discount = Decimal(0)
  shipping = Decimal(4)

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
  def get_order_for_store(store_slug):
    if store_slug in orders:
      return orders.get(store_slug)
    order = Order.objects.create(
      # Order
      subtotal = Decimal(0),
      tax = Decimal(0),
      delivery_window = delivery_window,

      # Meta
      invoice = invoice,
      status = Order.STATUS_PENDING,
    )
    orders[store_slug] = order
    return order

  # Fetch items from cart and db
  items = cart_items(json.loads(request.POST['ids']))
  allow_sub_detail = json.loads(request.POST['allow_sub_detail'])

  # Add order items and calculate subtotal and tax
  for wrap in items:
    item = wrap['obj']
    order = get_order_for_store(item.category.store.slug)

    allow_sub = allow_sub_detail[unicode(item.id)]
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
    "business": PAYPAL_RECEIVER_EMAIL,
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
    'sandbox': DEBUG,
  })
  return HttpResponse(template.render(context))
