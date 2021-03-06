from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions

from account.api.serializers import *

from order.models import Invoice
from order.api.serializers import InvoiceSerializer
from delivery.models import DeliveryBucket
from delivery.api.serializers import DeliveryBucketSerializer

# Views
class UserViewSet(viewsets.ReadOnlyModelViewSet):
  model = User
  serializer_class = UserSerializer
  ordering_fields = ['date_joined', 'last_login']

# Current user views
class CurrentUserView(generics.RetrieveAPIView):
  model = User
  serializer_class = UserSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_object(self):
    return self.request.user

class CurrentUserInvoicesView(generics.ListAPIView):
  serializer_class = InvoiceSerializer
  permission_classes = [permissions.IsAuthenticated]
  ordering = ['-when_created']
  ordering_fields = ['when_created', 'when_updated']

  def get_queryset(self):
    return Invoice.objects.filter(user=self.request.user)

class CurrentUserDeliveryBucketsView(generics.ListAPIView):
  serializer_class = DeliveryBucketSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return DeliveryBucket.objects.filter(assignee=self.request.user)

