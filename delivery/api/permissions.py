from rest_framework import permissions

def is_driver(request):
  return request.user.is_authenticated() and request.user.groups.filter(name='driver')

def is_manager(request):
  return request.user.is_authenticated() and request.user.groups.filter(name='delivery_manager')

def is_assignee(request, obj):
  return request.user.is_authenticated() and obj.assignee.pk == request.user.pk


class DeliveryBucketPermission(permissions.BasePermission):
  def has_permission(self, request, view):
    return view.action == 'retrieve' or is_manager(request)

  def has_object_permission(self, request, view, obj):
    return is_manager(request) or is_assignee(request, obj)

class DeliveryBucketOrderPermission(permissions.BasePermission):
  def has_permission(self, request, view):
    return is_driver(request)
