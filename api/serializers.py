from rest_framework import serializers

from django.contrib.auth.models import User
from shop.models import *
from order.models import *
from delivery.models import *

# Account
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined']

# Shop
class StoreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Store

class StoreCustomizationSerializer(serializers.ModelSerializer):
  class Meta:
    model = StoreCustomization

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category

class ItemListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Item

class ItemSerializer(serializers.ModelSerializer):
  category = CategorySerializer()
  class Meta:
    model = Item

# Order
class DeliveryWindowListSerializer(serializers.ModelSerializer):
  class Meta:
    model = DeliveryWindow

class DeliveryWindowSerializer(serializers.ModelSerializer):
  store = StoreSerializer()
  class Meta:
    model = DeliveryWindow

class InvoiceSerializer(serializers.ModelSerializer):
  orders = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
  user = UserSerializer()
  total = serializers.Field()
  class Meta:
    model = Invoice

class OrderItemSerializer(serializers.ModelSerializer):
  item = ItemSerializer()
  class Meta:
    model = OrderItem

class OrderListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order

class OrderSerializer(serializers.ModelSerializer):
  order_items = OrderItemSerializer()
  invoice = InvoiceSerializer()
  delivery_window = DeliveryWindowSerializer()
  delivery_buckets = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='deliverybucket-detail')
  total = serializers.Field()
  class Meta:
    model = Order

class CouponSerializer(serializers.ModelSerializer):
  class Meta:
    model = Coupon

# Delivery
class DeliveryBucketOrderSerializer(serializers.ModelSerializer):
  order = OrderSerializer()
  class Meta:
    model = DeliveryBucketOrder

class DeliveryBucketListSerializer(serializers.ModelSerializer):
  class Meta:
    model = DeliveryBucket

class DeliveryBucketSerializer(serializers.ModelSerializer):
  delivery_bucket_orders = DeliveryBucketOrderSerializer()
  assignor = UserSerializer()
  assignee = UserSerializer()
  class Meta:
    model = DeliveryBucket
