from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import Context, loader
from cart.models import Order
from datetime import datetime
import json
from django.shortcuts import render_to_response
from paypal.standard.forms import PayPalPaymentsForm
import time
import uuid
from home.views import computeSummaryInternal
from urllib import urlencode
from fruitex.config import DOMAIN
from fruitex.settings import PAYPAL_RECEIVER_EMAIL

def cart(request):
    return render_to_response("cart.html", {})

@csrf_exempt
def confirm(request):
    name = request.POST['name']
    phone = request.POST['phone']
    address = request.POST['address']
    postcode = request.POST['postcode']
    ids = request.POST['ids']
    deliveryWindow = request.POST['time']

    res = computeSummaryInternal(ids)
    price = res['sum']
    tax = res['tax']
    shipping = res['delivery']

    invoice = str(uuid.uuid4())
    Order(name=name, address=address, phone=phone, postcode=postcode,
        items=ids, price=price, tax=tax, shipping=shipping, status='pending',
        delivery_window = deliveryWindow, time=datetime.now(), invoice=invoice).save()
    paypal_dict = {
        "business": PAYPAL_RECEIVER_EMAIL,
        "currency_code": "CAD",
        "amount": "%.2f" % (float(price) + float(tax) + float(shipping)),
        "item_name": "fruitex order",
        "invoice": invoice,
        "notify_url": "http://%s/fruitex-magic-ipn/" % DOMAIN,
        "return_url": "http://%s/redir/?%s" % (DOMAIN, urlencode({"to" : "/check_order?invoice=" + invoice})),
        "return": "http://%s/return_page/" % DOMAIN,
        "cancel_return": "http://i%s/redir/?to=/home" % DOMAIN,
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
      'total': round(tax + shipping + price, 2),
    }
    return render_to_response("confirm.html", context)

