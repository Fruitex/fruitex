from django.http import HttpResponse
from django.template import Context, loader
from django.utils.timezone import make_aware, get_default_timezone, localtime
from django.utils.datastructures import SortedDict
from django.contrib.auth.decorators import login_required, user_passes_test

from datetime import datetime, timedelta
from itertools import chain
from decimal import Decimal

from order.models import DeliveryWindow, Invoice, Order

def can_user_view_delivery(user):
   if user:
      return user.groups.filter(name='driver').count() > 0
   return False

@login_required
@user_passes_test(can_user_view_delivery, login_url='/account/login')
def summary(request):
  def divide_delivery_window(delivery_windows, divider_func):
    divided = SortedDict()
    for delivery_window in delivery_windows:
      divider = divider_func(delivery_window)
      if divider in divided:
        divided[divider].append(delivery_window)
      else:
        divided[divider] = [delivery_window]
    return divided

  datetime_threshold = make_aware(datetime.now() - timedelta(days=60), get_default_timezone())
  delivery_windows = DeliveryWindow.objects.filter(start__gt=datetime_threshold).order_by('-start', 'store__id')
  delivery_windows = filter(lambda dw: len(dw.waiting_orders) != 0, delivery_windows)

  divider_func = lambda dw: localtime(dw.start).date().strftime("%b %d, %a")
  divided_by_date = divide_delivery_window(delivery_windows, divider_func)
  divider_func = lambda dw: localtime(dw.start).strftime("%H:%M") + '~' + localtime(dw.end).strftime("%H:%M")
  divided_by_date_and_time = [(day, divide_delivery_window(divided_by_date[day], divider_func)) for day in divided_by_date]

  context = Context({
    'delivery_windows_divided_by_date_and_time': divided_by_date_and_time,
  })

  template = loader.get_template('delivery/summary.html')
  return HttpResponse(template.render(context))

@login_required
@user_passes_test(can_user_view_delivery, login_url='/account/login')
def detail(request, id):
  def sorted_order_items(orders):
    order_items = chain.from_iterable(map(lambda order: order.order_items, orders))
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
  invoices = filter(lambda invoice: invoice.status in (Invoice.STATUS_PAID, Invoice.STATUS_PAY_ON_DELIVERY), invoices)

  context = Context({
    'invoices': invoices
  })

  template = loader.get_template('delivery/destinations.html')
  return HttpResponse(template.render(context))

def statistics(request):
  datetime_threshold = make_aware(datetime.now() - timedelta(days=60), get_default_timezone())
  orders = Order.objects.filter(when_created__gt=datetime_threshold).order_by('-delivery_window__start', 'delivery_window__id', 'status')
  dates = set(map(lambda order: order.delivery_window.start.date(), orders))
  dates = sorted(list(dates), reverse=True)

  def stats_for_date(date):
    date_orders = filter(lambda order: order.delivery_window.start.date() == date, orders)
    stores = set(map(lambda order: order.delivery_window.store, date_orders))
    def stats_for_store(store):
      store_orders = filter(lambda order: order.delivery_window.store == store, date_orders)
      normal_orders = filter(lambda order: order.status != Order.STATUS_PENDING, store_orders)
      pending_orders = filter(lambda order: order.status == Order.STATUS_PENDING, store_orders)
      return (
        store,
        len(store_orders),
        len(normal_orders),
        len(pending_orders),
        reduce(lambda acc, order: acc + order.subtotal, store_orders, Decimal('0')),
        reduce(lambda acc, order: acc + order.subtotal, normal_orders, Decimal('0')),
        reduce(lambda acc, order: acc + order.subtotal, pending_orders, Decimal('0')),
      )
    stats = map(stats_for_store, stores)
    return (date, stats)

  stats = map(stats_for_date, dates)

  template = loader.get_template('delivery/statistics.html')
  context = Context({
    'stats': stats,
  })
  return HttpResponse(template.render(context))

