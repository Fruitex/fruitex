from django.conf.urls import patterns, url

urlpatterns = patterns('order.views',
  # Views
  url(r'^new/$', 'new_order', name='new'),
)
