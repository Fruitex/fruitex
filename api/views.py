from rest_framework import viewsets

from api.serializers import *

from django.contrib.auth.models import User
from shop.models import *
from order.models import *
from delivery.models import *

# Account
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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

# Order
class DeliveryWindowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeliveryWindow.objects.all()
    serializer_class = DeliveryWindowSerializer

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

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
