from django.http import HttpResponse
from django.template import Context, loader
from home.models import Store, Item
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response,redirect
from cart.models import Order
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from home.views import toStructuredItem, getItemsByIds
from django.shortcuts import render
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
    'invoice': o.invoice,
    'allow_sub_detail':o.allow_sub_detail
	}

@login_required
def orders(request):
  template = loader.get_template('orders.html')
  context = Context({
    'orders': json.dumps(map(toStructuredOrder, Order.objects.exclude(status='pending')))
  })
  return HttpResponse(template.render(context));
@login_required
def norders(request):
  orders = Order.objects.filter(status__in=['paid','flagged']).order_by('-time')
  context_orders = []
  for o in orders:
    time = o.time
    co = toStructuredOrder(o)
    co['id'] = o.id
    co['time'] = o.time.strftime('%d, %B %Y %H:%M:%S')
    if co['allow_sub_detail']:
      co['allow_sub_detail'] = json.loads(co['allow_sub_detail'])
    else:
      co['allow_sub_detail'] = {}
    ids = co['items']
    ids_num = {}
    for id in ids:
      if id in ids_num:
        ids_num[id] = ids_num[id] + 1
      else:
        ids_num[id] = 1
    items = Item.objects.filter(id__in=ids_num.keys())
    order_items = []
    for item in items:
      if str(item.id) in co['allow_sub_detail']:
        allow_sub = co['allow_sub_detail'][str(item.id)]
      else:
        allow_sub = 1
      order_items.append({'category':item.category,'store':item.store.name,'allow_sub':allow_sub,'quatity':ids_num[item.id],'id':item.id,'name':item.name,'price':item.price,'sku':item.sku})
    co['context_items'] = order_items
    context_orders.append(co)
  context = Context({
    'orders':context_orders,
    'orders_json':json.dumps(context_orders)
  })
  return render(request,'norders.html',context)
def delivered(request):
    id = request.POST['id']
    order = Order.objects.filter(id=id)[0]
    order.status='delivered'
    order.save()
    return HttpResponse(json.dumps({'status':'ok'}))
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
    for i in range(0, ids.count(it['id'])):
      group_by_cate[c].append(it['id'])
  return HttpResponse(json.dumps(group_by_cate))

def get_orders_internal(invoices):
  return map(toStructuredOrder, Order.objects.filter(invoice__in=invoices))

def get_order_detail(order):
  time = order.time
  order = toStructuredOrder(order)
  order['time'] = time
  ids = order['items']
  ids_num = {}
  if order['allow_sub_detail']:
    allow_sub_detail = json.loads(order['allow_sub_detail'])
  else:
    allow_sub_detail = {}
  for id in ids:
    if id in ids_num:
      ids_num[id] = ids_num[id] + 1
    else:
      ids_num[id] = 1
  items = Item.objects.filter(id__in=ids_num.keys())
  order_items = {}
  for item in items:
    if str(item.id) in allow_sub_detail:
      allow_sub = allow_sub_detail[str(item.id)]
    else:
      allow_sub = 1;
    if item.store.id in order_items:
      order_items[item.store.id]['items'].append({'allow_sub':allow_sub,'quatity':ids_num[item.id],'id':item.id,'name':item.name,'price':item.price,'sku':item.sku})
    else:
      order_items[item.store.id] = {'id':item.store.id,'name':item.store.name,'address':item.store.address,'map':'map_'+item.store.name+'.png','items':[{'allow_sub':allow_sub,'quatity':ids_num[item.id],'id':item.id,'name':item.name,'price':item.price,'sku':item.sku}]}
  order['item_detail'] = order_items
  return order    
def check_order(request):
  if 'invoice' in request.GET:
    invoice = request.GET['invoice']
  else:
    return error(request)
  template = loader.get_template('check_order.html')
  order = Order.objects.filter(invoice=invoice)
  if len(order) == 0:
    return error(request)
  order_detail = get_order_detail(order[0])
  context = Context({
    'order':order_detail,
  })
  return HttpResponse(template.render(context));

def return_page(request):
    return render_to_response("return_page.html", {})

def browserNotSupport(request):
    return render_to_response("not_support.html", {})
