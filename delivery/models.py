from django.db import models
from django.utils.timezone import localtime


class DeliveryBucketOrder(models.Model):
  def __unicode__(self):
    return self.order + ' ' + self.delivery_bucket

  delivery_bucket = models.ForeignKey('DeliveryBucket')
  order = models.ForeignKey('order.Order')


class DeliveryBucket(models.Model):
  def __unicode__(self):
    start = localtime(self.start)
    end = localtime(self.end)
    return start.strftime(self.DATETIME_FORMAT) + " ~ " + end.strftime(self.DATETIME_FORMAT)

  DATETIME_FORMAT = '%a %b %d  %H:%M'

  start = models.DateTimeField()
  end = models.DateTimeField()
  driver = models.ForeignKey('auth.User', related_name='delivery_buckets')
  orders = models.ManyToManyField('order.Order', related_name='delivery_buckets', through=DeliveryBucketOrder)
