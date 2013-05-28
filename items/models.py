from django.db import models

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

class Item(models.Model):
    store = models.ForeignKey(Store)
    category = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    price = models.IntegerField()

