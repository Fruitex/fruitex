from django.contrib import admin
from home.models import Item
from home.models import Store

class StoreAdmin(admin.ModelAdmin):
  list_display = ["name", "id", "address"]
  ordering = [ "-id" ]
  search_fields = ["id", "name"]

admin.site.register(Store, StoreAdmin)

class ItemAdmin(admin.ModelAdmin):
  list_display = [
    "name", "id", "sku", "price", "sales_price", "store", "category",
    "sold_number", "out_of_stock"
  ]
  list_filter = [ "store", "out_of_stock", "tax_status", "tax_class" ]
  ordering = [ "-id" ]
  search_fields = ["id", "name", "sku"]

admin.site.register(Item, ItemAdmin)
