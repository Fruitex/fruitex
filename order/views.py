from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import Context, loader
from django.core import serializers
from paypal.standard.forms import PayPalPaymentsForm

from shop.models import Item
from order.models import Order, OrderItem
from config.paypal import PAYPAL_RECEIVER_EMAIL
from config.environment import DOMAIN,DEBUG

from decimal import Decimal
import urllib
import json
import uuid

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

@csrf_exempt
def view_cart(request):
  template = loader.get_template('order/cart.html')

  cart = cart_from_request(request)
  items = cart_items(cart)

  context = Context({
    'items': items,
  })
  return HttpResponse(template.render(context))

@csrf_exempt
def new_order(request):
  template = loader.get_template('order/show.html')

  # Gether info from POST to setup the order
  # Customer infos
  customer_name = request.POST['name']
  address = request.POST['address']
  postcode = request.POST['postcode']
  phone = request.POST['phone']
  email = request.POST['email']

  # Order infos
  invoice = str(uuid.uuid4())
  delivery_window = request.POST['time']
  coupon = request.POST['coupon']

  # Validate coupon
  # TODO
  discount = Decimal(0)
  shipping = Decimal(4)

  # Create order
  order = Order.objects.create(
    # Order
    invoice = invoice,
    delivery_window = delivery_window,
    subtotal = Decimal(0),
    tax = Decimal(0),
    shipping = shipping,
    discount = discount,

    # Metas
    status = Order.STATUS_PENDING,

    # Customer
    customer_name = customer_name,
    address = address,
    postcode = postcode,
    phone = phone,
    email = email,
  )

  # Fetch items from cart and db
  items = cart_items(json.loads(request.POST['ids']))
  allow_sub_detail = json.loads(request.POST['allow_sub_detail'])
  subtotal = Decimal(0);
  tax = Decimal(0);

  # Add order items and calculate subtotal and tax
  for wrap in items:
    item = wrap['obj']
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

    subtotal += item_cost
    tax += item_tax

  # Update subtotal and tax
  order.subtotal = subtotal
  order.tax = tax
  order.save()

  # Setup paypal dict
  paypal_dict = {
      "business": PAYPAL_RECEIVER_EMAIL,
      "currency_code": "CAD",
      "amount": "%.2f" % order.total,
      "item_name": "Fruitex order #%d" % order.id,
      "invoice": invoice,
      "notify_url": "http://%s/fruitex-magic-ipn/" % DOMAIN,
      "return_url": "http://%s/redir/?%s" % (DOMAIN, urllib.urlencode({"to" : "/check_order?invoice=" + invoice})),
      "cancel_return": "http://%s/redir/?to=/shop" % DOMAIN,
      "custom": json.dumps({'coupon': coupon})
  }

  # Create the Paypal form
  form = PayPalPaymentsForm(initial=paypal_dict)

  # Setup context and render
  context = Context({
    'order': order,
    'order_items': OrderItem.objects.filter(order__id=order.id),
    'form': form,
    'sandbox': DEBUG,
  })
  return HttpResponse(template.render(context))
