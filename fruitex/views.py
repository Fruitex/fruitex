from django.http import HttpResponse
from django.template import Context, loader
from home.models import Store, Item
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response,redirect
from cart.models import Order
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from home.views import toStructuredItem
import json

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


def toStructuredOrder(o):
	ids = json.loads(o.items)
	return {
		'name': o.name,
		'address': o.address,
		'postcode': o.postcode,
		'price': o.price,
		'tax': o.tax,
		'shipping': o.shipping,
		'phone': o.phone,
		'items': ids,
		'delivery_window': o.delivery_window,
		'time': o.time.isoformat(),
        'status': o.status,
	}

@login_required
def orders(request):
  template = loader.get_template('orders.html')
  context = Context({
    'orders': json.dumps(map(toStructuredOrder, Order.objects.exclude(status='pending')))
  })
  return HttpResponse(template.render(context));

@login_required
@csrf_exempt
def get_orders(request):
  if 'invoices' in request.POST:
    invoices = json.loads(request.POST['invoices'])
  else:
    return HttpResponse('error');
  return HttpResponse(json.dumps(get_orders_internal(invoices)))

@login_required
@csrf_exempt
def group_orders(request):
  if 'invoices' in request.POST:
    invoices = json.loads(request.POST['invoices'])
  else:
    return HttpResponse('error')
  ids = []
  for o in get_orders_internal(invoices):
    ids.extend(o['items'])
  group_by_cate = {}
  for it in getItemsByIds(ids):
    c = it['category']
    if c not in group_by_cate:
      group_by_cate[c] = []
    group_by_cate[c].append({'name':it['name'], 'quantity':ids.count(it['id'])})
  return HttpResponse(json.dumps(group_by_cate))

def get_orders_internal(invoices):
  return map(toStructuredOrder, Order.objects.filter(invoice__in=invoices))

def check_order(request):
  if 'invoice' in request.GET:
    invoice = request.GET['invoice']
  else:
    return error(request)
  template = loader.get_template('check_order.html')
  context = Context({
    'order': json.dumps(toStructuredOrder(Order.objects.filter(invoice=invoice)[0])),
  })
  return HttpResponse(template.render(context));

def return_page(request):
    return render_to_response("return_page.html", {})

def browserNotSupport(request):
    return render_to_response("not_support.html", {})

