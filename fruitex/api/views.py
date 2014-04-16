from rest_framework import viewsets

class ChildModelViewSetMixin(viewsets.ReadOnlyModelViewSet):
  def list(self, request, *args, **kwargs):
    if self.parent_model:
      parent__name = self.parent_model.__name__.lower()
      key = parent__name + '__pk'
      parent__pk = kwargs.get(key)
    if parent__pk:
      filter_kwargs = {}
      filter_kwargs[parent__name] = parent__pk
      self.queryset = self.model.objects.filter(**filter_kwargs)
    else:
      self.queryset = None
    return super(ChildModelViewSetMixin, self).list(self, request)
