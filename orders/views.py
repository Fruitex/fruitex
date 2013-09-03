from django.http import HttpResponse
from django.template import Context, loader
from cart.models import Order
from home.models import Store, Item
import json
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from fruitex.views import error

def toStructuredItem(it):
	return {'name' : it.name, 'price' : it.price, 'category' : it.category, 
	'store' : it.store.id, 'id' : it.id, 'tax_class' : it.tax_class, 
	'sku' : it.sku, 'store': it.store.name }


def toStructuredOrder(o):
	ids = json.loads(o.items)
	its = Item.objects.filter(id__in = ids)
	items = []
	for it in its:
		item = toStructuredItem(it)
		item['quatity'] = ids.count(item['id'])
		items.append(item)
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
def orderlist(request):
  template = loader.get_template('order_manager.html')
  context = Context({
    'orders': json.dumps(map(toStructuredOrder, Order.objects.exclude(status='pending')))
  })
  return HttpResponse(template.render(context));

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
