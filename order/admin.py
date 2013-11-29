from django.contrib import admin
from order.models import Order, OrderItem, Coupon

class OrderAdmin(admin.ModelAdmin):
  date_hierarchy = 'when_placed'
  list_display = [
    'invoice', 'id', 'customer_name', 'email', 'status', 'total',
    'delivery_window', 'when_placed'
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
