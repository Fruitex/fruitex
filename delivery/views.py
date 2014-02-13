from django.http import HttpResponse
from django.template import Context, loader
from django.utils.timezone import make_aware, get_default_timezone, localtime
from django.utils.datastructures import SortedDict

from datetime import datetime, timedelta

from order.models import DeliveryWindow, Invoice

def summary(request):
  def divide_delivery_window(delivery_windows, divider_func):
    divided = {}
    for delivery_window in delivery_windows:
      divider = divider_func(delivery_window)
      if divider in divided:
        divided[divider].append(delivery_window)
      else:
        divided[divider] = [delivery_window]
    return divided

  datetime_threshold = make_aware(datetime.now() - timedelta(days=60), get_default_timezone())
  delivery_windows = DeliveryWindow.objects.filter(start__gt=datetime_threshold).order_by('-start', 'store__id')
  
  divider_func = lambda dw: localtime(dw.start).date().strftime("%b %d, %a")
  divided_by_days = divide_delivery_window(delivery_windows, divider_func)
  divider_func = lambda dw: localtime(dw.start).strftime("%H:%M") + '~' + localtime(dw.end).strftime("%H:%M")
  divided_by_time = dict([(day, divide_delivery_window(divided_by_days[day], divider_func)) for day in divided_by_days])
  
  divided_delivery_windows = sorted(divided_by_time.items(), reverse=True)
  divided_delivery_windows_ids = [dict([(time, day[1][time]) for time in day[1]]) for day in divided_delivery_windows]

  context = Context({
    'delivery_windows_divided_by_days_and_time': divided_delivery_windows,
  })

  template = loader.get_template('delivery/summary.html')
  return HttpResponse(template.render(context))

def detail(request, id):
  def sorted_order_items(orders):
    order_items = reduce(lambda acc, order: acc.extend(order.order_items), orders, [])
    order_items = sorted(order_items, key=lambda order_item: order_item.item.id)
    order_items = sorted(order_items, key=lambda order_item: order_item.item.category.shop_order)
    return order_items

  delivery_window = DeliveryWindow.objects.get(id=id)
  invoices = filter(lambda invoice: invoice.status in (Invoice.STATUS_PAID, Invoice.STATUS_PAY_ON_DELIVERY), map(lambda order: order.invoice, delivery_window.orders.all()))

  context = Context({
    'delivery_window': delivery_window,
    'order_items': sorted_order_items(delivery_window.waiting_orders),
    'invoices': invoices,
  })

  template = loader.get_template('delivery/detail.html')
  return HttpResponse(template.render(context))

def destinations(request, ids):
  delivery_window_ids = map(lambda s: int(s), ids.split('+'))
  delivery_windows = DeliveryWindow.objects.filter(id__in=delivery_window_ids)
  orders = map(lambda delivery_window: delivery_window.orders.all(), delivery_windows)
  orders = reduce(list.__add__, map(lambda order: list(order), orders))
  invoices = list(set(map(lambda order: order.invoice, orders)))
  
  context = Context({
    'invoices': invoices
  })
  
  template = loader.get_template('delivery/destinations.html')
  return HttpResponse(template.render(context))
