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
  actions = ["remove_sales_prices"]

  def remove_sales_prices(self, request, queryset):
    rows_updated = queryset.update(sales_price=-1.0)
    if rows_updated == 1:
        message_bit = "1 item's sales price was"
    else:
        message_bit = "%s items' sales prices were" % rows_updated
    self.message_user(request, "%s successfully removed." % message_bit)
  remove_sales_prices.short_description = "Remove sales prices"


admin.site.register(Item, ItemAdmin)
