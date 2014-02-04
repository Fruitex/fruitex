from django.http import HttpResponse
from django.template import Context, loader
from django.utils.timezone import make_aware, get_default_timezone, localtime
from django.utils.datastructures import SortedDict

from datetime import datetime, timedelta

from order.models import DeliveryWindow, Order

def summary(request):
  def divide_delivery_window_by_days(delivery_windows):
    divided = {}
    for delivery_window in delivery_windows:
      date = localtime(delivery_window.start).date()
      if date in divided:
        divided[date].append(delivery_window)
      else:
        divided[date] = [delivery_window]
    return divided

  datetime_threshold = make_aware(datetime.now() - timedelta(days=30), get_default_timezone())
  delivery_windows = DeliveryWindow.objects.filter(start__gt=datetime_threshold).order_by('-start', 'store__id')
  divided_by_days = divide_delivery_window_by_days(delivery_windows)

  context = Context({
    'delivery_windows': delivery_windows,
    'delivery_windows_divided_by_days': sorted(divided_by_days.items(), reverse=True),
  })

  template = loader.get_template('delivery/summary.html')
  return HttpResponse(template.render(context))

def detail(request, id):
  def combine_items(orders):
    items = {}
    for order in orders:
      if order.status == Order.STATUS_PENDING:
        continue
      for order_item in order.order_items:
        if order_item.item in items:
          items[order_item.item] += order_item.quantity
        else:
          items[order_item.item] = order_item.quantity
    items = SortedDict(map(lambda x: (x, items[x]), sorted(items.keys(), key=lambda item: item.category.shop_order)))
    return items

  delivery_window = DeliveryWindow.objects.get(id=id)

  context = Context({
    'delivery_window': delivery_window,
    'combined_items': combine_items(delivery_window.orders.all())
  })

  template = loader.get_template('delivery/detail.html')
  return HttpResponse(template.render(context))
