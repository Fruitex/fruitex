from django.db import models

# Create your models here.
class Order(models.Model):
    def __unicode__(self):
        return self.invoice
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    postcode = models.CharField(max_length=10)
    items = models.CharField(max_length=1000)
    price = models.FloatField()
    tax = models.FloatField()
    shipping = models.FloatField()
    status = models.CharField(max_length=20)
    delivery_window = models.CharField(max_length=20)
    time = models.DateTimeField()
    invoice = models.CharField(max_length=30)
    sub_type = models.CharField(max_length=30,default='')
    allow_sub_detail = models.CharField(max_length=2000)
    email = models.CharField(max_length=64,default='')

class Coupon(models.Model):
  def __unicode__(self):
    return self.code
  code = models.CharField(max_length=30)
  value = models.FloatField()
  used = models.BooleanField()
