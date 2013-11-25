from django.contrib import admin
from shop.models import Store
from shop.models import Category
from shop.models import Item

class StoreAdmin(admin.ModelAdmin):
  list_display = ['name', 'id', 'address']
  ordering = ['-id']
  search_fields = ['id', 'name']

admin.site.register(Store, StoreAdmin)

class CategoryAdmin(admin.ModelAdmin):
  list_display = ['__unicode__', 'id', 'store']
  ordering = ['store', 'parent']
  search_fields = ['__unicode__']
  list_filter = ['store']

admin.site.register(Category, CategoryAdmin)

class ItemAdmin(admin.ModelAdmin):
  date_hierarchy = 'when_added'
  list_display = [
    'name', 'id', 'price', 'sales_price', 'category',
    'sold_number', 'out_of_stock', 'on_sale'
  ]
  list_filter = [ 'category', 'out_of_stock', 'on_sale', 'tax_class' ]
  ordering = [ '-id' ]
  search_fields = ['id', 'name', 'sku']
  actions = ['remove_sales']

  def remove_sales(self, request, queryset):
    rows_updated = queryset.update(on_sale=False)
    if rows_updated == 1:
        message_bit = "1 item was "
    else:
        message_bit = "%s items were" % rows_updated
    self.message_user(request, "%s successfully marked as not on sale." % message_bit)
  remove_sales.short_description = "Mark as not on sale"

admin.site.register(Item, ItemAdmin)
