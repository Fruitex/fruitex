from django.db import models
from jsonfield import JSONField

class Store(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=50)
    address = models.TextField()

class Category(models.Model):
    def __unicode__(self):
        if self.parent is None:
            return self.name
        return self.parent.unicode() + '->' + self.name
    name = models.CharField(max_length=100)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='categories')
    parent = models.ForeignKey('Category', blank=True, null=True)

class Item(models.Model):
    def __unicode__(self):
        return self.name

    # Tax Classes
    TAX_CLASSES = (
        ('NT', 'Non-Taxable'),
        ('SR', 'Standard-Rate'),
        ('ZR', 'Zero-Rate'),
    )

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='items')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2, default='', blank=True)
    out_of_stock = models.BooleanField(default=False)
    sku = models.CharField(max_length=20)
    tax_class = models.CharField(max_length=2, choices=TAX_CLASSES, default='NT')
    meta = JSONField()
    sold_number = models.IntegerField(default=0)
    when_added = models.DateTimeField(auto_now_add=True)
    when_updated = models.DateTimeField(auto_now=True)
