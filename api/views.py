from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import *

import django_filters

from api.serializers import *

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from shop.models import *
from order.models import *
from delivery.models import *

class ReadOnlyListRetrieveModelViewSet(viewsets.ReadOnlyModelViewSet):
  # derived classes must have a field 'instance_serializer'
  def retrieve(self, request, pk=None):
    instance = get_object_or_404(self.queryset, pk=pk)
    serializer = self.instance_serializer(instance)
    return Response(serializer.data)

# Filters
class ItemFilter(django_filters.FilterSet):
  min_sold = django_filters.NumberFilter(name="sold_number", lookup_type='gte')
  max_sold = django_filters.NumberFilter(name="sold_number", lookup_type='lte')
  class Meta:
    model = Item
    fields = ['on_sale', 'out_of_stock', 'featured', 'sold_number', 'min_sold', 'max_sold']

class OrderFilter(django_filters.FilterSet):
  created_after = django_filters.DateTimeFilter(name="when_created", lookup_type='gt')
  created_before = django_filters.DateTimeFilter(name="when_created", lookup_type='lt')
  updated_after = django_filters.DateTimeFilter(name="when_updated", lookup_type='gt')
  updated_before = django_filters.DateTimeFilter(name="when_updated", lookup_type='lt')
  class Meta:
    model = Order
    fields = ['status', 'invoice__invoice_num', 'created_after', 'created_before', 'updated_after', 'updated_before']

class InvoiceFilter(django_filters.FilterSet):
  created_after = django_filters.DateTimeFilter(name="when_created", lookup_type='gt')
  created_before = django_filters.DateTimeFilter(name="when_created", lookup_type='lt')
  updated_after = django_filters.DateTimeFilter(name="when_updated", lookup_type='gt')
  updated_before = django_filters.DateTimeFilter(name="when_updated", lookup_type='lt')
  class Meta:
    model = Invoice
    fields = ['status', 'email', 'user__username', 'created_after', 'created_before', 'updated_after', 'updated_before']

class DeliveryBucketFilter(django_filters.FilterSet):
  after = django_filters.DateTimeFilter(name="end", lookup_type='gt')
  before = django_filters.DateTimeFilter(name="start", lookup_type='lt')
  class Meta:
    model = DeliveryBucket
    fields = ['assignee__username', 'assignee__id', 'after', 'before']

# Account
class UserViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  ordering_fields = ['date_joined', 'last_login']

# Shop
class StoreViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Store.objects.all()
  serializer_class = StoreSerializer

class StoreCustomizationViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = StoreCustomization.objects.all()
  serializer_class = StoreCustomizationSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer

class ItemViewSet(ReadOnlyListRetrieveModelViewSet):
  queryset = Item.objects.all()
  serializer_class = ItemListSerializer
  instance_serializer = ItemSerializer
  filter_class = ItemFilter
  ordering_fields = ['sold_number']

# Order
class DeliveryWindowViewSet(ReadOnlyListRetrieveModelViewSet):
  queryset = DeliveryWindow.objects.all()
  serializer_class = DeliveryWindowListSerializer
  instance_serializer = DeliveryWindowSerializer

class OrderViewSet(ReadOnlyListRetrieveModelViewSet):
  queryset = Order.objects.all()
  serializer_class = OrderListSerializer
  instance_serializer = OrderSerializer
  filter_class = OrderFilter
  ordering = ['-when_created']
  ordering_fields = ['when_created', 'when_updated', 'subtotal']

class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Invoice.objects.all()
  serializer_class = InvoiceSerializer
  filter_class = InvoiceFilter
  ordering = ['-when_created']
  ordering_fields = ['when_created', 'when_updated', 'subtotal']

class CouponViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Coupon.objects.all()
  serializer_class = CouponSerializer

# Delivery
class DeliveryBucketViewSet(ReadOnlyListRetrieveModelViewSet):
  renderer_classes = (JSONRenderer, JSONPRenderer, BrowsableAPIRenderer)
  queryset = DeliveryBucket.objects.all()
  serializer_class = DeliveryBucketListSerializer
  instance_serializer = DeliveryBucketSerializer
  filter_class = DeliveryBucketFilter
  ordering = ['-start']
