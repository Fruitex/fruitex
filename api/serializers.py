from rest_framework import serializers

from django.contrib.auth.models import User
from shop.models import *
from order.models import *
from delivery.models import *

# Account
class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'url', 'username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined']

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
  store = StoreSerializer()
  class Meta:
    model = DeliveryWindow

class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
  total = serializers.Field()
  class Meta:
    model = Invoice

class OrderItemSerializer(serializers.ModelSerializer):
  item = ItemSerializer()
  class Meta:
    model = OrderItem

class OrderSerializer(serializers.HyperlinkedModelSerializer):
  order_items = OrderItemSerializer()
  delivery_window = DeliveryWindowSerializer()
  delivery_buckets = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='deliverybucket-detail')
  class Meta:
    model = Order

class CouponSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Coupon

# Delivery
class DeliveryBucketOrderSerializer(serializers.ModelSerializer):
  order = OrderSerializer()
  class Meta:
    model = DeliveryBucketOrder

class DeliveryBucketSerializer(serializers.HyperlinkedModelSerializer):
  delivery_bucket_orders = DeliveryBucketOrderSerializer()
  assignor = UserSerializer()
  assignee = UserSerializer()
  class Meta:
    model = DeliveryBucket
    fields = ['start', 'end', 'assignor', 'assignee', 'delivery_bucket_orders']
