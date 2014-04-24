from rest_framework import serializers

from account.api.serializers import UserSerializer
from shop.api.serializers import StoreSerializer, ItemSerializer
from order.models import *

# Serializers
class DeliveryWindowSerializer(serializers.ModelSerializer):
  store = StoreSerializer()
  class Meta:
    model = DeliveryWindow

class InvoiceSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  orders = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
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
  total = serializers.Field()
  delivery_window = DeliveryWindowSerializer()
  class Meta:
    model = Order
