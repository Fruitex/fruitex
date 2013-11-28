from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core import serializers

from shop.models import Item

import urllib
import json

# Common operations

def cart_from_request(request):
  cart = urllib.unquote(request.COOKIES.get('cart'))
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

def new_order(request):
  return HttpResponse('not implemented')
