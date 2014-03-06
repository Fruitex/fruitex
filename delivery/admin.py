from django.contrib import admin
from delivery.models import DeliveryBucket

class DeliveryBucketAdmin(admin.ModelAdmin):
  date_hierarchy = 'start'
  list_display = [
    'start', 'end', 'driver'
  ]
  ordering = [ '-start' ]
  search_fields = ['start', 'driver']

admin.site.register(DeliveryBucket, DeliveryBucketAdmin)
