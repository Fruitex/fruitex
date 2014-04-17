from rest_framework.viewsets import ReadOnlyModelViewSet
from order.api.permissions import InvoicePermission, OrderPermission, DeliveryWindowPermission
import django_filters

from order.models import *
from order.api.serializer import *

# Filters
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
    fields = ['status', 'email', 'user__id', 'user__username', 'created_after', 'created_before', 'updated_after', 'updated_before']


# Views
class OrderViewSet(ReadOnlyModelViewSet):
  model = Order
  serializer_class = OrderSerializer
  permission_classes = [OrderPermission]
  filter_class = OrderFilter
  ordering = ['-when_created']
  ordering_fields = ['when_created', 'when_updated', 'subtotal']

class InvoiceViewSet(ReadOnlyModelViewSet):
  model = Invoice
  serializer_class = InvoiceSerializer
  permission_classes = [InvoicePermission]
  filter_class = InvoiceFilter
  ordering = ['-when_created']
  ordering_fields = ['when_created', 'when_updated', 'subtotal']

class DeliveryWindowViewSet(ReadOnlyModelViewSet):
  model = DeliveryWindow
  serializer_class = DeliveryWindowSerializer
  permission_classes = [DeliveryWindowPermission]
