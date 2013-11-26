from django.conf.urls import patterns, url

urlpatterns = patterns('shop.views',
  url(r'^$', 'to_default', name='to_default'),
  url(r'^(?P<store_slug>\w+)/$', 'store_home', name='store_home'),
  url(r'^(?P<store_slug>\w+)/category/(?P<category_id>\d+)/$', 'store_category', name='store_category'),
)
