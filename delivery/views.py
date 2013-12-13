from django.http import HttpResponse
from django.template import Context, loader
from django.utils.timezone import make_aware, get_default_timezone

from datetime import datetime, timedelta

from order.models import DeliveryWindow

def summary(request):
  datetime_threshold = make_aware(datetime.now() - timedelta(days=30), get_default_timezone())
  delivery_windows = DeliveryWindow.objects.filter(start__gt=datetime_threshold)

  context = Context({
    'delivery_windows': delivery_windows,
  })

  template = loader.get_template('delivery/summary.html')
  return HttpResponse(template.render(context))

def detail(request, id):
  def combine_items(orders):
    items = {}
    for order in orders:
      for order_item in order.order_items:
        if order_item.item in items:
          items[order_item.item] += order_item.quantity
        else:
          items[order_item.item] = order_item.quantity
    return items

  delivery_window = DeliveryWindow.objects.get(id=id)

  context = Context({
    'delivery_window': delivery_window,
    'combined_items': combine_items(delivery_window.orders.all())
  })

  template = loader.get_template('delivery/detail.html')
  return HttpResponse(template.render(context))
