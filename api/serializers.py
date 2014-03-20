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
  delivery_buckets = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='deliverybucket-detail')
  class Meta:
    model = Order

class CouponSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Coupon

# Delivery

class DeliveryBucketDeliveryWindowSerializer(serializers.HyperlinkedModelSerializer):
  store = StoreSerializer()
  class Meta:
    model = DeliveryWindow

class DeliveryBucketOrderSerializer(serializers.HyperlinkedModelSerializer):
  order_items = OrderItemSerializer()
  invoice = InvoiceSerializer()
  delivery_window = DeliveryBucketDeliveryWindowSerializer()
  class Meta:
    model = Order
    fields = ['invoice', 'status', 'when_created', 'when_updated', 'order_items', 'subtotal', 'comment', 'delivery_window']

class DeliveryBucketSerializer(serializers.HyperlinkedModelSerializer):
  orders = DeliveryBucketOrderSerializer(many=True)
  assignor = UserSerializer()
  assignee = UserSerializer()
  class Meta:
    model = DeliveryBucket
