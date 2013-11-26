from django.db import models

class Store(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=50)
    slug = models.SlugField()
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

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='items')
    sku = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    out_of_stock = models.BooleanField(default=False)
    on_sale = models.BooleanField(default=False)
    tax_class = models.CharField(max_length=2, choices=TAX_CLASSES, default='NT')
    sold_number = models.IntegerField(editable=False, default=0)
    when_added = models.DateTimeField(auto_now_add=True)
    when_updated = models.DateTimeField(auto_now=True)

class ItemMeta(models.Model):
    def __unicode__(self):
        return self.key + ': ' + self.value
    item = models.ForeignKey(Item, related_name="metas")
    key = models.CharField(max_length=256)
    value = models.CharField(max_length=256)
