from django.contrib import admin

from delivery.models import DeliveryBucket, DeliveryBucketOrder

class DeliveryBucketOrderInline(admin.TabularInline):
  model = DeliveryBucketOrder
  raw_id_fields = ['delivery_bucket', 'order']

class DeliveryBucketAdmin(admin.ModelAdmin):
  date_hierarchy = 'start'
  list_display = ['start', 'end', 'driver']
  ordering = [ '-start' ]
  search_fields = ['start', 'driver']
  inlines = [DeliveryBucketOrderInline]

admin.site.register(DeliveryBucket, DeliveryBucketAdmin)
