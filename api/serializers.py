from rest_framework import serializers

from django.contrib.auth.models import User
from shop.models import *
from order.models import *
from delivery.models import *

# Account
class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'url', 'username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined')

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
  delivery_buckets = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='deliverybucket-detail')
  class Meta:
    model = Order

class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = OrderItem

class CouponSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Coupon

# Delivery
class DeliveryBucketSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = DeliveryBucket
