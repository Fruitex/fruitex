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
  user = UserSerializer()
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
  class Meta:
    model = Order
