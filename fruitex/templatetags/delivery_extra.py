from django import template

register = template.Library()

@register.filter(name='join_by_attr')
def join_by_attr(list, attr):
  return '+'.join(unicode(getattr(i, attr)) for i in list)
