from django.db import models
from django.utils.timezone import localtime

from datetime import date

from order import managers, emails

class Invoice(models.Model):
  def __unicode__(self):
    return self.invoice_num

  def _get_total(self):
    return self.subtotal + self.tax + self.delivery - self.discount;

  def set_status(self, status):
    if status == self.STATUS_PAID or status == self.STATUS_FLAGGED or status == self.STATUS_PAY_ON_DELIVERY:
      for order in self.orders.all():
        order.status = Order.STATUS_WAITING
        order.save()
    self.status = status
    self.save()
    emails.send_order_received(self)

  # Status
  STATUS_PENDING = 'PEND'
  STATUS_PAID = 'PAID'
  STATUS_FLAGGED = 'FLAG'
  STATUS_CANCELLED = 'CANC'
  STATUS_PAY_ON_DELIVERY = 'POD'
  STATUSES = (
    (STATUS_PENDING, 'Pending'),
    (STATUS_PAID, 'Paid'),
    (STATUS_FLAGGED, 'Flagged'),
    (STATUS_CANCELLED, 'Cancelled'),
    (STATUS_PAY_ON_DELIVERY, 'Pay on Delivery')
  )

  invoice_num = models.CharField(max_length=64, unique=True)
  status = models.CharField(max_length=4, choices=STATUSES)
  payer = models.CharField(max_length=256, blank=True)
  when_created = models.DateTimeField(auto_now_add=True)
  when_updated = models.DateTimeField(auto_now=True)
  coupon = models.ForeignKey('Coupon', blank=True, null=True)

  # Amounts
  subtotal = models.DecimalField(max_digits=16, decimal_places=2)
  tax = models.DecimalField(max_digits=16, decimal_places=2)
  delivery = models.DecimalField(max_digits=16, decimal_places=2)
  discount = models.DecimalField(max_digits=16, decimal_places=2)
  total = property(_get_total)

  # Customer
  customer_name = models.CharField(max_length=64)
  address = models.TextField()
  postcode = models.CharField(max_length=16)
  phone = models.CharField(max_length=16)
  email = models.EmailField(max_length=256)
  user = models.ForeignKey('auth.User', blank=True, null=True, related_name='invoices', on_delete=models.SET_NULL)

class Payment(models.Model):
  def __unicode__(self):
    return str(self.id)

  def set_status(self, status):
    if status == self.STATUS_COMPLETED:
      self.invoice.set_status(Invoice.STATUS_PAID)
    if status == self.STATUS_CANCELLED:
      self.invoice.set_status(Invoice.STATUS_CANCELLED)
    self.status = status
    self.save()

  # Payment methods
  METHODS_PAYPAL = 'PP'
  METHODS_SQUARE = 'SQ'
  METHODS = (
    (METHODS_PAYPAL, 'Paypal'),
    (METHODS_SQUARE, 'Square (pay on delivery)'),
  )

  # Payment status
  STATUS_CREATED = 'CREA'
  STATUS_COMPLETED = 'COMP'
  STATUS_CANCELLED = 'CANC'
  STATUSES = (
    (STATUS_CREATED, 'Created'),
    (STATUS_COMPLETED, 'Completed'),
    (STATUS_CANCELLED, 'Cancelled'),
  )

  invoice = models.ForeignKey('Invoice', related_name='payments')
  method = models.CharField(max_length=2, choices=METHODS)
  status = models.CharField(max_length=4, choices=STATUSES, default=STATUS_CREATED)
  amount = models.DecimalField(max_digits=16, decimal_places=2)
  raw = models.TextField(blank=True)
  when_created = models.DateTimeField(auto_now_add=True)
  when_updated = models.DateTimeField(auto_now=True)

  objects = managers.PaymentManager()


class DeliveryWindow(models.Model):
  def __unicode__(self):
    start = localtime(self.start)
    end = localtime(self.end)
    return start.strftime(self.DATETIME_FORMAT) + " ~ " + end.strftime(self.DATETIME_FORMAT)

  DATETIME_FORMAT = '%a %b %d  %H:%M'

  store = models.ForeignKey('shop.Store', related_name='delivery_windows')
  start = models.DateTimeField()
  end = models.DateTimeField()

  objects = managers.DeliveryWindowManager()


class OrderItem(models.Model):
  def __unicode__(self):
    return str(self.item) + ' * ' + str(self.quantity)

  order = models.ForeignKey('Order')
  item = models.ForeignKey('shop.Item')
  quantity = models.IntegerField()
  allow_sub = models.BooleanField()
  item_cost = models.DecimalField(max_digits=16, decimal_places=2)
  item_tax = models.DecimalField(max_digits=16, decimal_places=2)


class Order(models.Model):
  def __unicode__(self):
    return '#' + str(self.id)

  def _get_order_items(self):
    return OrderItem.objects.filter(order__id=self.id)

  # Status
  STATUS_PENDING = 'PEND'                 # Pending until invoice has been paid
  STATUS_WAITING = 'WAIT'                 # Waiting for the delivery time
  STATUS_PURCHASED = 'PURC'               # Item's has been purchased and packed
  STATUS_ON_THE_WAY = 'ONTW'              # Delivery on its way
  STATUS_DELIVERED = 'DELI'               # Order delivered
  STATUSES = (
    (STATUS_PENDING, 'Pending'),
    (STATUS_WAITING, 'Waiting'),
    (STATUS_PURCHASED, 'Purchased'),
    (STATUS_ON_THE_WAY, 'On the way'),
    (STATUS_DELIVERED, 'Delivered'),
  )

  # Order
  items = models.ManyToManyField('shop.Item', related_name='orders', through=OrderItem)
  order_items = property(_get_order_items)
  subtotal = models.DecimalField(max_digits=16, decimal_places=2)
  tax = models.DecimalField(max_digits=16, decimal_places=2)
  delivery_window = models.ForeignKey('DeliveryWindow', related_name='orders', on_delete=models.PROTECT)
  comment = models.TextField()

  # Metas
  invoice = models.ForeignKey('Invoice', related_name='orders', on_delete=models.PROTECT)
  status = models.CharField(max_length=4, choices=STATUSES)
  when_created = models.DateTimeField(auto_now_add=True)
  when_updated = models.DateTimeField(auto_now=True)


class Coupon(models.Model):
  def __unicode__(self):
    return self.code

  # Coupon types
  TYPE_FIXED_AMOUNT = 'FIX'
  TYPE_PERCENTAGE = 'PERC'
  TYPES = (
    (TYPE_FIXED_AMOUNT, 'Fixed amount'),
    (TYPE_PERCENTAGE, 'Percentage'),
  )

  objects = managers.CouponManager()

  code = models.CharField(max_length=32, unique=True)
  type = models.CharField(max_length=4, choices=TYPES)
  value = models.DecimalField(max_digits=16, decimal_places=2)
  used = models.BooleanField()
  expire = models.DateField(blank=True, default=date.max)
