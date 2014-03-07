from django.contrib import admin
from django.contrib.auth.models import User

from delivery.models import DeliveryBucket, DeliveryBucketOrder

class DeliveryBucketOrderInline(admin.TabularInline):
  model = DeliveryBucketOrder
  raw_id_fields = ['delivery_bucket', 'order']

class DeliveryBucketAdmin(admin.ModelAdmin):
  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'driver':
      kwargs['queryset'] = User.objects.filter(groups__name__contains='driver')
    return super(DeliveryBucketAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

  date_hierarchy = 'start'
  list_display = ['start', 'end', 'driver']
  ordering = [ '-start' ]
  search_fields = ['start', 'driver']
  inlines = [DeliveryBucketOrderInline]

admin.site.register(DeliveryBucket, DeliveryBucketAdmin)
