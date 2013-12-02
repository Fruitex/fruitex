from django.contrib import admin
from order.models import Invoice, Order, OrderItem, Coupon

class InvoiceAdmin(admin.ModelAdmin):
  date_hierarchy = 'when_created'
  list_display = [
    'invoice_num', 'status', 'payer', 'total', 'when_created'
  ]
  list_filter = [ 'status' ]
  search_fields = ['invoice', 'payer']

admin.site.register(Invoice, InvoiceAdmin)

class OrderAdmin(admin.ModelAdmin):
  date_hierarchy = 'when_placed'
  list_display = [
    'id', 'customer_name', 'email', 'status', 'delivery_window',
    'when_updated',
  ]
  list_filter = [ 'status' ]
  ordering = [ '-when_placed' ]
  search_fields = ['id', 'invoice', 'customer_name', 'email', 'phone', 'address', 'postcode']

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
  list_display = [ 'code', 'id', 'value', 'used' ]
  list_filter = [ 'used' ]
  ordering = [ '-id' ]
  search_fields = [ 'code' ]

admin.site.register(Coupon, CouponAdmin)
