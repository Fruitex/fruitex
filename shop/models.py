from django.db import models
from decimal import Decimal
from datetime import datetime, timedelta

from shop.managers import ItemMetaFilterManager

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
    display_order = models.IntegerField(default=0)

class StoreCustomization(models.Model):
    def __unicode__(self):
        return self.store.name

    def _get_featured_display_name(self):
        return self.featured.replace('_', ' ').replace('-', ' ').title()

    store = models.OneToOneField(Store, related_name='customization')
    featured = models.CharField(max_length=200, default='', blank=True)
    show_banner = models.BooleanField(default=False)
    show_on_sale = models.BooleanField(default=False)
    show_best_selling = models.BooleanField(default=True)

    featured_display_name = property(_get_featured_display_name)


class DeliveryOption(models.Model):
    def __unicode__(self):
        return self.get_display_name()

    def _get_weekday_availability(self):
        return reduce(lambda a, d: a + (str(d + 1) if self.valid_for_weekday(d) else '-'), xrange(7), '')

    def get_display_name(self, now=None):
        now = now if now is not None else datetime.now()
        start = datetime(now.year, now.month, now.day) + timedelta(minutes=self.start_time)
        end = start + timedelta(minutes=self.time_interval)
        return self.display_format\
                    .replace('{start_date}', start.strftime(self.DATE_FORMAT))\
                    .replace('{start_time}', start.strftime(self.TIME_FORMAT))\
                    .replace('{end_date}', end.strftime(self.DATE_FORMAT))\
                    .replace('{end_time}', end.strftime(self.TIME_FORMAT))

    def is_in_effect(self, now=None):
        now = now if now is not None else datetime.now()
        start = datetime(now.year, now.month, now.day) + timedelta(minutes=self.start_time)
        diff = start - now
        return self.valid_for_weekday(now.weekday()) and (diff.days * 1440 + (diff.seconds / 60)) > DeliveryOption.EFFECTIVE_THRESHOLD

    def valid_for_weekday(self, weekday):
        switch = {
            0: self.monday,
            1: self.tuesday,
            2: self.wednesday,
            3: self.thursday,
            4: self.friday,
            5: self.saturday,
            6: self.sunday,
        }
        return switch.get(weekday)

    # Delivery option lost effect one hour before the start time
    EFFECTIVE_THRESHOLD = 60
    DATE_FORMAT = '%a %b %d'
    TIME_FORMAT = '%H:%M'

    store = models.ForeignKey('Store', related_name='delivery_options')
    name = models.CharField(max_length=100)
    display_format = models.CharField(max_length=256, default='{start_date} {start_time} ~ {end_time}')
    display_name = property(get_display_name)

    # Start time: Number of minutes since the beginning of the day
    start_time = models.IntegerField()
    time_interval = models.IntegerField()

    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=True)
    sunday = models.BooleanField(default=True)
    weekday_availability = property(_get_weekday_availability)

    cost = models.DecimalField(max_digits=16, decimal_places=2)
    in_effect = property(is_in_effect)


class Category(models.Model):
    def __unicode__(self):
        if self.parent is None:
            return self.name
        return self.parent.__unicode__() + '->' + self.name

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    icon = models.CharField(max_length=100, blank=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='categories')
    parent = models.ForeignKey('Category', blank=True, null=True, related_name='sub_categories')

    # Shopping info
    shop_order = models.IntegerField(default=0)
    shop_location_note = models.TextField(default='', blank=True)


class Item(models.Model):
    def __unicode__(self):
        return self.name

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return type(self) == type(other) and (self.id) == (other.id)

    def increase_sold_number(self, quantity):
        self.sold_number += quantity
        self.save()

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
    max_quantity_per_order = models.IntegerField(default=0)
    featured = models.CharField(max_length=200, default='', blank=True)
    sold_number = models.IntegerField(editable=False, default=0)
    when_added = models.DateTimeField(auto_now_add=True)
    when_updated = models.DateTimeField(auto_now=True)


class ItemMetaFilter(models.Model):
    def __unicode__(self):
        return self.key

    key = models.CharField(max_length=256)
    filterable = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)

    objects = ItemMetaFilterManager()


class ItemMeta(models.Model):
    def __unicode__(self):
        return self.key + ': ' + self.value

    def _get_filter(self):
        return ItemMetaFilter.objects.get(key=self.key)

    item = models.ForeignKey(Item, related_name="metas")
    key = models.CharField(max_length=256)
    value = models.CharField(max_length=256)
    filter = property(_get_filter)
