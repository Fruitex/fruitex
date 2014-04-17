from django.contrib.auth.models import User
from rest_framework import viewsets

from account.api.serializers import *

# Views
class UserViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  ordering_fields = ['date_joined', 'last_login']

  def dispatch(self, request, *args, **kwargs):
    if kwargs.get('pk') == 'current' and request.user.is_authenticated():
        kwargs['pk'] = request.user.pk

    return super(UserViewSet, self).dispatch(request, *args, **kwargs)
