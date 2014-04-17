from rest_framework import serializers

from account.api.serializers import UserSerializer
from order.api.serializers import OrderSerializer
from delivery.models import *

# Serializers
class DeliveryBucketSerializer(serializers.ModelSerializer):
  assignor = UserSerializer()
  assignee = UserSerializer()
  class Meta:
    model = DeliveryBucket

class DeliveryBucketOrderSerializer(serializers.ModelSerializer):
  order = OrderSerializer()
  class Meta:
    model = DeliveryBucketOrder
