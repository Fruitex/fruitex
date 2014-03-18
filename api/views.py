from rest_framework import viewsets
import django_filters

from api.serializers import *

from django.contrib.auth.models import User
from shop.models import *
from order.models import *
from delivery.models import *

# Filters
class ItemFilter(django_filters.FilterSet):
    min_sold = django_filters.NumberFilter(name="sold_number", lookup_type='gte')
    max_sold = django_filters.NumberFilter(name="sold_number", lookup_type='lte')
    class Meta:
        model = Item
        fields = ['on_sale', 'out_of_stock', 'featured', 'sold_number', 'min_sold', 'max_sold']

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

class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_class = ItemFilter
    ordering_fields = ['sold_number']

# Order
class DeliveryWindowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeliveryWindow.objects.all()
    serializer_class = DeliveryWindowSerializer

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_fields = ['status', 'invoice__invoice_num']
    ordering = ['-when_created']
    ordering_fields = ['when_created', 'when_updated', 'subtotal']

class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filter_fields = ['status', 'email', 'user__username']
    ordering = ['-when_created']
    ordering_fields = ['when_created', 'when_updated', 'subtotal']

class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class CouponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

# Delivery
class DeliveryBucketViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeliveryBucket.objects.all()
    serializer_class = DeliveryBucketSerializer
    ordering = ['-start']
