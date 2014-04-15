from django.contrib.auth.models import User
from rest_framework import serializers

# Serializers
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined']
