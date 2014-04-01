from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets
from order.models import Invoice, Payment, DeliveryWindow, Order, OrderItem, Coupon
from delivery.models import DeliveryBucket

class ReadonlyAdmin(admin.ModelAdmin):
  def get_readonly_fields(self, request, obj=None):
    if request.user.is_superuser:
      return self.readonly_fields
    if self.declared_fieldsets:
      return flatten_fieldsets(self.declared_fieldsets)
    return list(set(
        [field.name for field in self.opts.local_fields] +
        [field.name for field in self.opts.local_many_to_many]
    ))

class OrderInline(admin.TabularInline):
  model = Order
  raw_id_fields = ['invoice']
  fields = [
    'status', 'invoice', 'comment', 'subtotal', 'tax'
  ]
  readonly_fields = [
    'invoice', 'comment', 'subtotal', 'tax'
  ]
  extra = 0

class PaymentInline(admin.TabularInline):
  model = Payment
  fields = [
    'method', 'status', 'amount', 'when_created', 'when_updated'
  ]
  readonly_fields = fields
  extra = 0

class InvoiceAdmin(ReadonlyAdmin):
  date_hierarchy = 'when_created'
  list_display = [
    'invoice_num', 'customer_name', 'email', 'status', 'total', 'user', 'when_created'
  ]
  list_filter = [ 'status' ]
  raw_id_fields = ['coupon']
  ordering = [ '-when_created' ]
  search_fields = ['invoice_num', 'customer_name', 'email', 'phone', 'address', 'postcode', 'user__username']
  inlines = [OrderInline, PaymentInline]

admin.site.register(Invoice, InvoiceAdmin)

class PaymentAdmin(ReadonlyAdmin):
  date_hierarchy = 'when_created'
  list_display = [
    'id', 'invoice', 'method', 'status', 'amount', 'when_created', 'when_updated'
  ]
  list_filter = [ 'method', 'status' ]
  ordering = [ '-when_created' ]
  search_fields = ['invoice__invoice_num', 'amount']

admin.site.register(Payment, PaymentAdmin)

class DeliveryWindowAdmin(ReadonlyAdmin):
  def create_delivery_bucket(self, request, queryset):
    for window in queryset:
      DeliveryBucket.objects.create_bucket_from_window(window, request.user, request.user)
    self.message_user(request, "%d delivery bucket has been created." % queryset.count())

  date_hierarchy = 'start'
  list_display = [
    '__unicode__', 'store', 'start', 'end'
  ]
  ordering = [ '-start', 'store__id' ]
  search_fields = ['store', 'start', 'end']
  actions = ['create_delivery_bucket']
  inlines = [OrderInline]

admin.site.register(DeliveryWindow, DeliveryWindowAdmin)

class OrderItemInline(admin.TabularInline):
  model = OrderItem
  fields = [
    'item', 'quantity', 'allow_sub', 'item_cost', 'item_tax'
  ]
  readonly_fields = fields
  extra = 0

class OrderAdmin(ReadonlyAdmin):
  date_hierarchy = 'when_created'
  list_display = [
    'id', 'invoice', 'status', 'delivery_window', 'when_created',
  ]
  list_filter = [ 'status' ]
  raw_id_fields = ['delivery_window', 'invoice']
  ordering = [ '-when_created' ]
  search_fields = ['id', 'invoice__invoice_num']
  inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(ReadonlyAdmin):
  list_display = [
    'id', 'item', 'order', 'quantity', 'allow_sub',
    'item_cost', 'item_tax'
  ]
  list_filter = [ 'allow_sub' ]
  ordering = [ '-id' ]
  search_fields = ['id', 'item__name', 'order__id']
  raw_id_fields = ['order', 'item']

admin.site.register(OrderItem, OrderItemAdmin)

class CouponAdmin(ReadonlyAdmin):
  list_display = [ 'code', 'id', 'type', 'value', 'used' ]
  list_filter = [ 'type', 'used' ]
  ordering = [ '-id' ]
  search_fields = [ 'code' ]

admin.site.register(Coupon, CouponAdmin)
