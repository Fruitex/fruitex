from django.contrib import admin
from order.models import Invoice, Payment, DeliveryWindow, Order, OrderItem, Coupon
from delivery.models import DeliveryBucket

class InvoiceAdmin(admin.ModelAdmin):
  date_hierarchy = 'when_created'
  list_display = [
    'invoice_num', 'customer_name', 'email', 'status', 'total', 'when_created'
  ]
  list_filter = [ 'status' ]
  raw_id_fields = ['coupon']
  ordering = [ '-when_created' ]
  search_fields = ['invoice', 'payer', 'customer_name', 'email', 'phone', 'address', 'postcode']

admin.site.register(Invoice, InvoiceAdmin)

class PaymentAdmin(admin.ModelAdmin):
  date_hierarchy = 'when_created'
  list_display = [
    'id', 'invoice', 'method', 'status', 'amount', 'when_created', 'when_updated'
  ]
  list_filter = [ 'method', 'status' ]
  ordering = [ '-when_created' ]
  search_fields = ['invoice', 'amount']

admin.site.register(Payment, PaymentAdmin)

class DeliveryWindowAdmin(admin.ModelAdmin):
  def create_delivery_bucket(self, request, queryset):
    for window in queryset:
      DeliveryBucket.objects.create_bucket_from_window(window, request.user)
    self.message_user(request, "%d delivery bucket has been created." % queryset.count())

  date_hierarchy = 'start'
  list_display = [
    '__unicode__', 'store', 'start', 'end'
  ]
  ordering = [ '-start', 'store__id' ]
  search_fields = ['store', 'start', 'end']
  actions = ['create_delivery_bucket']

admin.site.register(DeliveryWindow, DeliveryWindowAdmin)

class OrderAdmin(admin.ModelAdmin):
  date_hierarchy = 'when_created'
  list_display = [
    'id', 'invoice', 'status', 'delivery_window', 'when_created',
  ]
  list_filter = [ 'status' ]
  raw_id_fields = ['delivery_window', 'invoice']
  ordering = [ '-when_created' ]
  search_fields = ['id', 'invoice__invoice_num']

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
  list_display = [
    'id', 'item', 'order', 'quantity', 'allow_sub',
    'item_cost', 'item_tax'
  ]
  list_filter = [ 'allow_sub' ]
  ordering = [ '-id' ]
  search_fields = ['id', 'item__name', 'order__id']
  raw_id_fields = ['order', 'item']

admin.site.register(OrderItem, OrderItemAdmin)

class CouponAdmin(admin.ModelAdmin):
  list_display = [ 'code', 'id', 'type', 'value', 'used' ]
  list_filter = [ 'type', 'used' ]
  ordering = [ '-id' ]
  search_fields = [ 'code' ]

admin.site.register(Coupon, CouponAdmin)
