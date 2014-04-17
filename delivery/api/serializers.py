from rest_framework import serializers

from account.api.serializers import UserSerializer
from order.api.serializers import OrderSerializer
from delivery.models import *

# Serializers
class DeliveryBucketOrderSerializer(serializers.ModelSerializer):
  order = OrderSerializer()
  class Meta:
    model = DeliveryBucketOrder

class DeliveryBucketSerializer(serializers.ModelSerializer):
  delivery_bucket_orders = DeliveryBucketOrderSerializer()
  assignor = UserSerializer()
  assignee = UserSerializer()
  class Meta:
    model = DeliveryBucket
