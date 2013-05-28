from django.db import models

# Create your models here.
class Store(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)

class Item(models.Model):
    def __unicode__(self):
        return self.name
    store = models.ForeignKey(Store)
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    sku = models.CharField(max_length=20)
    tax_status = models.CharField(max_length=50)
    tax_class = models.CharField(max_length=50)
    remark = models.CharField(max_length=200)

