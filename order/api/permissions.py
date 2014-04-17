from rest_framework import permissions

class InvoicePermission(permissions.BasePermission):
  """
  Permission check for user property
  """

  def is_driver(self, request):
    return request.user.is_authenticated() and request.user.groups.filter(name='driver')

  def is_owner(self, request, obj):
    return request.user.is_authenticated() and obj.user.pk == request.user.pk

  def has_permission(self, request, view):
    return view.action == 'retrieve' or self.is_driver(request)

  def has_object_permission(self, request, view, obj):
    return obj.user is None or self.is_driver(request) or self.is_owner(request, obj)
