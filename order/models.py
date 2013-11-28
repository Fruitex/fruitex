from django.db import models

class OrderItem(models.Model):
  order = models.ForeignKey('Order')
  item = models.ForeignKey('shop.Item')
  quantity = models.IntegerField()
  allow_sub = models.BooleanField()


class Order(models.Model):
  def __unicode__(self):
      return self.invoice

  def _get_total(self):
    return self.subtotal + self.tax + self.shipping - self.discount;

  # Tax Classes
  STATUS_PENDING = 'PEND'
  STATUS_PAID = 'PAID'
  STATUS_FLAGGED = 'FLAG'
  STATUS_DELIVERED = 'DELI'
  STATUSES = (
    (STATUS_PENDING, 'Pending'),
    (STATUS_PAID, 'Paid'),
    (STATUS_FLAGGED, 'Flagged'),
    (STATUS_DELIVERED, 'Delivered'),
  )

  # Order
  invoice = models.CharField(max_length=32, unique=True)
  items = models.ManyToManyField('shop.Item', related_name='orders', through=OrderItem)
  delivery_window = models.CharField(max_length=32)
  subtotal = models.DecimalField(max_digits=16, decimal_places=2)
  tax = models.DecimalField(max_digits=16, decimal_places=2)
  shipping = models.DecimalField(max_digits=16, decimal_places=2)
  discount = models.DecimalField(max_digits=16, decimal_places=2)
  total = property(_get_total)

  # Metas
  status = models.CharField(max_length=4, choices=STATUSES)
  when_placed = models.DateTimeField(auto_now_add=True)
  when_updated = models.DateTimeField(auto_now=True)

  # Customer
  customer_name = models.CharField(max_length=64)
  address = models.TextField()
  postcode = models.CharField(max_length=16)
  phone = models.CharField(max_length=16)
  email = models.EmailField(max_length=128)


class Coupon(models.Model):
  def __unicode__(self):
    return self.code
  code = models.CharField(max_length=32)
  value = models.DecimalField(max_digits=16, decimal_places=2)
  used = models.BooleanField()
