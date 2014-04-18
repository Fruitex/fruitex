from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions

from account.api.serializers import *

# Views
class UserViewSet(viewsets.ReadOnlyModelViewSet):
  model = User
  serializer_class = UserSerializer
  ordering_fields = ['date_joined', 'last_login']

class CurrentUserView(generics.RetrieveAPIView):
  model = User
  serializer_class = UserSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_object(self):
    return self.request.user
