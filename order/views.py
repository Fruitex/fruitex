from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader

from shop.models import Item

import urllib
import json

# Views

@csrf_exempt
def new_order(request):
  cart = urllib.unquote(request.COOKIES.get('cart'))
  cart = json.loads(cart)
  return HttpResponse(json.dumps(cart))
