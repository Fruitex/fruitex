from rest_framework import viewsets
import django_filters

from fruitex.api.views import ChildModelViewSetMixin
from shop.models import *
from shop.api.serializer import *

# Filters
class ItemFilter(django_filters.FilterSet):
  min_sold = django_filters.NumberFilter(name="sold_number", lookup_type='gte')
  max_sold = django_filters.NumberFilter(name="sold_number", lookup_type='lte')
  class Meta:
    model = Item
    fields = ['on_sale', 'out_of_stock', 'featured', 'sold_number', 'min_sold', 'max_sold']

# Views
class StoreViewSet(viewsets.ReadOnlyModelViewSet):
  model = Store
  serializer_class = StoreSerializer

class CategoryViewSet(ChildModelViewSetMixin, viewsets.ReadOnlyModelViewSet):
  model = Category
  parent_model = Store
  serializer_class = CategorySerializer

class ItemViewSet(ChildModelViewSetMixin, viewsets.ReadOnlyModelViewSet):
  model = Item
  parent_model = Category
  serializer_class = ItemSerializer
  filter_class = ItemFilter
  ordering_fields = ['sold_number']
