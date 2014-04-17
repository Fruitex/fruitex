from rest_framework import viewsets
import re

def convert_camel(name):
  s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
  return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

class ChildModelViewSetMixin(viewsets.ReadOnlyModelViewSet):
  def list(self, request, *args, **kwargs):
    if self.parent_model:
      parent__name = convert_camel(self.parent_model.__name__)
      key = parent__name + '__pk'
      parent__pk = kwargs.get(key)
    if parent__pk:
      filter_kwargs = {}
      filter_kwargs[parent__name] = parent__pk
      self.queryset = self.model.objects.filter(**filter_kwargs)
    else:
      self.queryset = None
    return super(ChildModelViewSetMixin, self).list(self, request)
