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

class OrderSerializer(serializers.ModelSerializer):
  invoice = InvoiceSerializer()
  total = serializers.Field()
  delivery_window = DeliveryWindowSerializer()
  class Meta:
    model = Order

class OrderItemSerializer(serializers.ModelSerializer):
  item = ItemSerializer()
  class Meta:
    model = OrderItem
