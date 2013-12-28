from django.db import models
from decimal import Decimal
from datetime import datetime, timedelta
from operator import attrgetter
from itertools import chain

class Store(models.Model):
    def __unicode__(self):
        return self.name

    def __hash__(self):
        return hash(self.slug)

    def __eq__(self, other):
        return type(self) == type(other) and (self.slug, self.address) == (other.slug, other.address)

    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    address = models.TextField()


class DeliveryOption(models.Model):
    def __unicode__(self):
        return self.name

    def _is_in_effect(self):
        now = datetime.now()
        start = datetime(now.year, now.month, now.day) + timedelta(minutes=self.start_time)
        diff = start - now
        return (((diff.days * 86400) + diff.seconds) / 60) > DeliveryOption.EFFECTIVE_THRESHOLD

    # Delivery option lost effect one hour before the start time
    EFFECTIVE_THRESHOLD = 60

    store = models.ForeignKey('Store', related_name='delivery_options')
    name = models.CharField(max_length=100)
    # Start time: Number of minutes since the beginning of the day
    start_time = models.IntegerField()
    time_interval = models.IntegerField()
    cost = models.DecimalField(max_digits=16, decimal_places=2)
    in_effect = property(_is_in_effect)


class Category(models.Model):
    def __unicode__(self):
        if self.parent is None:
            return self.name
        return self.parent.__unicode__() + '->' + self.name

    def item_meta_keys(self, include_parent=True):
        keys = self.categoryitemmetakey_set.order_by('display_order')
        if include_parent and self.parent is not None:
            parent_keys = self.parent.item_meta_keys()
            keys = sorted(chain(parent_keys, keys), key=attrgetter('display_order'))
        return keys

    def raw_item_metas(self):
        keys = self.item_meta_keys()
        values = map(lambda key: key.item_meta_values(category=self), keys)
        return {k: v for k, v in zip(keys, values)}

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    icon = models.CharField(max_length=100, blank=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='categories')
    parent = models.ForeignKey('Category', blank=True, null=True, related_name='sub_categories')


class Item(models.Model):
    def __unicode__(self):
        return self.name

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return type(self) == type(other) and (self.id) == (other.id)


    # Tax Classes
    TAX_CLASSES = (
        (Decimal('0.0'), 'Non-Taxable'),
        (Decimal('0.13'), 'Standard-Rate'),
    )

    name = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='items')
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    sales_price = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    tax_class = models.DecimalField(max_digits=3, decimal_places=2, choices=TAX_CLASSES, default=Decimal('0.0'))
    out_of_stock = models.BooleanField(default=False)
    on_sale = models.BooleanField(default=False)
    featured = models.CharField(max_length=200, default='', blank=True)
    sold_number = models.IntegerField(editable=False, default=0)
    when_added = models.DateTimeField(auto_now_add=True)
    when_updated = models.DateTimeField(auto_now=True)


class ItemMeta(models.Model):
    def __unicode__(self):
        return self.key + ': ' + self.value
    item = models.ForeignKey(Item, related_name="metas")
    key = models.CharField(max_length=256)
    value = models.CharField(max_length=256)


class CategoryItemMetaKey(models.Model):
    def __unicode__(self):
        return self.key

    def item_meta_values(self, include_children=False, category=None):
        if category is None:
            category = self.category
        values = ItemMeta.objects.filter(
            key__iexact=self.key, item__category=category
        ).values_list('value', flat=True).distinct()
        if include_children:
            for child in self.category.sub_categories.all():
                values += child.item_meta_keys.item_meta_values(include_children)
            values = list(set(values))
        return values

    category = models.ForeignKey('Category')
    key = models.CharField(max_length=256)
    filterable = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
