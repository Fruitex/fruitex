from django.contrib import admin
from django.contrib.auth.models import User

from delivery.models import DeliveryBucket, DeliveryBucketOrder

class DeliveryBucketOrderInline(admin.TabularInline):
  model = DeliveryBucketOrder
  raw_id_fields = ['delivery_bucket', 'order']

class DeliveryBucketAdmin(admin.ModelAdmin):
  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'assignee':
      kwargs['queryset'] = User.objects.filter(groups__name__contains='driver')
    return super(DeliveryBucketAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

  def save_model(self, request, delivery_bucket, form, change):
    # Record assignor
    delivery_bucket.assignor = request.user
    delivery_bucket.save()

  date_hierarchy = 'start'
  list_display = ['__unicode__', 'start', 'end', 'assignee', 'assignor']
  readonly_fields = ['assignor']
  ordering = [ '-start', 'assignee' ]
  search_fields = ['start', 'assignee']
  inlines = [DeliveryBucketOrderInline]

admin.site.register(DeliveryBucket, DeliveryBucketAdmin)
