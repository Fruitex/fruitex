from rest_framework import serializers

from shop.models import *
from order.models import *

# Shop
class StoreSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Store

class StoreCustomizationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = StoreCustomization

class CategorySerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Category

class ItemSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Item

# Order
class DeliveryWindowSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = DeliveryWindow

class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
  total = serializers.Field()
  class Meta:
    model = Invoice

class OrderSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Order

class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = OrderItem

class CouponSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Coupon
