from rest_framework import mixins
import re

def convert_camel_to_snake(name):
  s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
  return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

class ChildrenListModelMixin(mixins.ListModelMixin):
  def list(self, request, *args, **kwargs):
    if self.parent_model:
      parent__name = self.parent_model.__name__.lower()
      parent__name_camel = convert_camel_to_snake(self.parent_model.__name__)
      key = parent__name + '__pk'
      parent__pk = kwargs.get(key)
    if parent__pk:
      filter_kwargs = {}
      filter_kwargs[parent__name_camel] = parent__pk
      self.queryset = self.model.objects.filter(**filter_kwargs)
    else:
      self.queryset = None
    return super(ChildrenListModelMixin, self).list(self, request)
