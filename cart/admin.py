from django.contrib import admin
from cart.models import Order,Coupon

class OrderAdmin(admin.ModelAdmin):
  date_hierarchy = "time"
  list_display = [
    "invoice", "id", "name",
    "email", "phone", "address", "postcode",
    "status", "delivery_window", "time"
  ]
  list_filter = [ "status", "sub_type" ]
  ordering = [ "-time" ]
  search_fields = ["id", "invoice", "email", "phone", "name", "address", "postcode"]

admin.site.register(Order, OrderAdmin)

class CouponAdmin(admin.ModelAdmin):
  list_display = [ "code", "id", "value", "used" ]
  list_filter = [ "used" ]
  ordering = [ "-id" ]
  search_fields = [ "code", "value" ]

admin.site.register(Coupon, CouponAdmin)
