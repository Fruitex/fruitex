from rest_framework import permissions

def is_driver(request):
  return request.user.is_authenticated() and request.user.groups.filter(name='driver')

def is_owner(request, obj):
  return request.user.is_authenticated() and obj.user.pk == request.user.pk


class InvoicePermission(permissions.BasePermission):
  """
  Permission check for user property
  """

  def has_permission(self, request, view):
    return view.action == 'retrieve' or is_driver(request)

  def has_object_permission(self, request, view, obj):
    return obj.user is None or is_driver(request) or is_owner(request, obj)

class OrderPermission(InvoicePermission):
  """
  Permission check for user property
  """

  def has_permission(self, request, view):
    return view.action == 'retrieve' or is_driver(request)

  def has_object_permission(self, request, view, obj):
    return super(OrderPermission, self).has_object_permission(request, view, obj.invoice)
