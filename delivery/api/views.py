from rest_framework import viewsets, renderers

import django_filters

from fruitex.api.views import ChildrenListModelMixin
from delivery.models import *
from delivery.api.serializers import *
from delivery.api.permissions import *

# Filters
class DeliveryBucketFilter(django_filters.FilterSet):
  after = django_filters.DateTimeFilter(name="end", lookup_type='gt')
  before = django_filters.DateTimeFilter(name="start", lookup_type='lt')
  class Meta:
    model = DeliveryBucket
    fields = ['assignee__username', 'assignee__id', 'after', 'before']


# Views
class DeliveryBucketViewSet(viewsets.ReadOnlyModelViewSet):
  renderer_classes = (
    renderers.JSONRenderer,
    renderers.JSONPRenderer,
    renderers.BrowsableAPIRenderer)
  model = DeliveryBucket
  serializer_class = DeliveryBucketSerializer
  permission_classes = [DeliveryBucketPermission]
  filter_class = DeliveryBucketFilter
  ordering = ['-start']

class DeliveryBucketOrderViewSet(ChildrenListModelMixin, viewsets.ReadOnlyModelViewSet):
  renderer_classes = (
    renderers.JSONRenderer,
    renderers.JSONPRenderer,
    renderers.BrowsableAPIRenderer)
  model = DeliveryBucketOrder
  parent_model = DeliveryBucket
  serializer_class = DeliveryBucketOrderSerializer
  permission_classes = [DeliveryBucketOrderPermission]
