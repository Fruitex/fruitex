from rest_framework import serializers

from account.api.serializer import UserSerializer
from shop.api.serializer import StoreSerializer, ItemSerializer
from order.models import *

# Serializers
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

class OrderSerializer(serializers.ModelSerializer):
  order_items = OrderItemSerializer()
  invoice = InvoiceSerializer()
  delivery_window = DeliveryWindowSerializer()
  delivery_buckets = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='deliverybucket-detail')
  total = serializers.Field()
  class Meta:
    model = Order
