from django.http import HttpResponse
from django.template import Context, loader
from home.models import Store, Item
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from cart.models import Order
from django.contrib.auth import authenticate

def home(request):
    return render_to_response("index.html", {})

def error(request):
    return render_to_response("error.html", {})

@csrf_exempt
def redir(request):
  if 'to' in request.GET:
    return redirect('%s' % request.GET['to'])
  else:
    return error(request)

@csrf_exempt
def checkout_return(request):
    invoice=request.GET['invoice']
    return render_to_response("checkout_return.html", {'invoice' : invoice})

@csrf_exempt
def check_order(request):
  if 'invoice' in request.GET:
    invoice = request.GET['invoice']
  else:
    invoice = ''
  orders = []
  for o in Order.objects.filter(invoice=invoice):
      orders.append(o)
  if len(orders) == 0:
      return error(request)
  else:
      return render_to_response("check_order.html", {'order' : orders[0]})

