from django.db import models
from django.utils.timezone import localtime

class DeliveryBucketOrder(models.Model):
  def __unicode__(self):
    return str(self.order) + ' @ ' + str(self.delivery_bucket)

  delivery_bucket = models.ForeignKey('DeliveryBucket')
  order = models.ForeignKey('order.Order')

class DeliveryBucketManager(models.Manager):
  def create_bucket_from_window(self, window, assignee, assignor):
    delivery_bucket = self.create(start = window.start, end = window.end, assignee = assignee, assignor = assignor)
    for order in window.orders.all():
      DeliveryBucketOrder.objects.create(delivery_bucket = delivery_bucket, order = order)
    return delivery_bucket

class DeliveryBucket(models.Model):
  def __unicode__(self):
    start = localtime(self.start)
    end = localtime(self.end)
    return start.strftime(self.DATETIME_FORMAT) + ' ~ ' + end.strftime(self.DATETIME_FORMAT) + ' (' + str(self.assignee) + ')'

  DATETIME_FORMAT = '%a %b %d  %H:%M'

  start = models.DateTimeField()
  end = models.DateTimeField()
  orders = models.ManyToManyField('order.Order', related_name='delivery_buckets', through=DeliveryBucketOrder)
  assignee = models.ForeignKey('auth.User', related_name='delivery_buckets')
  assignor = models.ForeignKey('auth.User', related_name='managed_delivery_buckets')

  objects = DeliveryBucketManager()
