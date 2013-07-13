from django.db import models

# Create your models here.
class Order(models.Model):
    def __unicode__(self):
        return "%s: %s %s" % (self.name, self.address, self.status)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    postcode = models.CharField(max_length=10)
    items = models.CharField(max_length=10)
    price = models.FloatField()
    tax = models.FloatField()
    shipping = models.FloatField()
    status = models.CharField(max_length=20)

