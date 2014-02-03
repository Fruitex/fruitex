from django.conf import settings
from django import template

register = template.Library()

@register.filter
def dict_val(d, key):
  try:
    value = d[key]
  except KeyError:
    value = settings.TEMPLATE_STRING_IF_INVALID

  return value
