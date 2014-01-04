from django.db import models

class ItemMetaFilterManager(models.Manager):
  def meta_filters_for_items(self, items):
    all_filterable_keys = map(lambda filter: filter.key, self.filter(filterable=True))
    values = {}
    for item in items.all():
      for meta in item.metas.all():
        if meta.key not in all_filterable_keys:
          continue
        value_set = values.get(meta.key)
        if value_set is None:
          values[meta.key] = set([meta.value])
        elif meta.key not in value_set:
          value_set.add(meta.value)
    return values
