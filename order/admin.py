from django.contrib import admin
from order.models import Invoice, Order, OrderItem, Coupon

class InvoiceAdmin(admin.ModelAdmin):
  date_hierarchy = 'when_created'
  list_display = [
    'invoice_num', 'customer_name', 'email', 'status', 'total', 'when_created'
  ]
  list_filter = [ 'status' ]
  ordering = [ '-when_created' ]
  search_fields = ['invoice', 'payer', 'customer_name', 'email', 'phone', 'address', 'postcode']

admin.site.register(Invoice, InvoiceAdmin)

class OrderAdmin(admin.ModelAdmin):
  date_hierarchy = 'when_created'
  list_display = [
    'id', 'invoice', 'status', 'delivery_window', 'when_created',
  ]
  list_filter = [ 'status' ]
  ordering = [ '-when_created' ]
  search_fields = ['id', 'invoice']

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
  list_display = [
    'id', 'item', 'order', 'quantity', 'allow_sub',
    'item_cost', 'item_tax'
  ]
  list_filter = [ 'allow_sub' ]
  ordering = [ '-id' ]
  search_fields = ['id', 'item', 'order']
  raw_id_fields = ['order', 'item']

admin.site.register(OrderItem, OrderItemAdmin)

class CouponAdmin(admin.ModelAdmin):
  list_display = [ 'code', 'id', 'type', 'value', 'used' ]
  list_filter = [ 'type', 'used' ]
  ordering = [ '-id' ]
  search_fields = [ 'code' ]

admin.site.register(Coupon, CouponAdmin)
