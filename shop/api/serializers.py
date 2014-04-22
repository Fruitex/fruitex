from rest_framework import serializers

from shop.models import *

# Serializers
class StoreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Store

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category

class ItemSerializer(serializers.ModelSerializer):
  category = CategorySerializer()
  class Meta:
    model = Item
