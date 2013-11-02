from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import Context, loader
from cart.models import Order, Coupon
from datetime import datetime
from datetime import timedelta
import json
from django.shortcuts import render_to_response
from paypal.standard.forms import PayPalPaymentsForm
import time
import uuid
from home.views import computeSummaryInternal
from urllib import urlencode
from fruitex.config import DOMAIN,DEBUG
from fruitex.settings import PAYPAL_RECEIVER_EMAIL

def cart(request):
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    return render_to_response("cart.html", {'today':today,'tomorrow':tomorrow})

@csrf_exempt
def confirm(request):

    name = request.POST['name']
    phone = request.POST['phone']
    address = request.POST['address']
    postcode = request.POST['postcode']
    ids = request.POST['ids']
    allow_sub_detail = request.POST['allow_sub_detail']
    deliveryWindow = request.POST['time']
    coupon = request.POST['coupon']
    res = computeSummaryInternal(ids, coupon)
    price = res['sum']
    tax = res['tax']
    shipping = res['delivery']
    discount = res['discount']
    total = max(float(price) + float(tax) + float(shipping) - float(discount), 0)
    invoice = str(uuid.uuid4())
    Order(name=name, address=address, phone=phone, postcode=postcode,
        items=ids, allow_sub_detail=allow_sub_detail,price=price, tax=tax, shipping=shipping, status='pending',
        delivery_window = deliveryWindow, time=datetime.now(), invoice=invoice).save()
    paypal_dict = {
        "business": PAYPAL_RECEIVER_EMAIL,
        "currency_code": "CAD",
        "amount": "%.2f" % total,
        "item_name": "fruitex order",
        "invoice": invoice,
        "notify_url": "http://%s/fruitex-magic-ipn/" % DOMAIN,
        "return_url": "http://%s/redir/?%s" % (DOMAIN, urlencode({"to" : "/check_order?invoice=" + invoice})),
        "return": "http://%s/return_page/" % DOMAIN,
        "cancel_return": "http://i%s/redir/?to=/home" % DOMAIN,
        "custom": json.dumps({'coupon': coupon})
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
      'name' : name,
      'ids' : ids,
      'phone' : phone,
      'address' : address,
      'postcode' : postcode,
      'phone' : phone,
      'price' : price,
      'tax' : tax,
      'delivery' : shipping,
      'delivery_window' : deliveryWindow,
      'invoice' : invoice,
      'form': form,
      'discount': discount,
      'total': round(total, 2),
      'sandbox': DEBUG,
      'allow_sub_detail':allow_sub_detail
    }
    return render_to_response("confirm.html", context)

