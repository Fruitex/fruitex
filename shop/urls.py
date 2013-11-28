from django.conf.urls import patterns, url

urlpatterns = patterns('shop.views',
  # Views
  url(r'^$', 'to_default', name='to_default'),
  url(r'^(?P<store_slug>\w+)/$', 'store_home', name='store_home'),
  url(r'^(?P<store_slug>\w+)/category/(?P<category_id>\d+)/$', 'store_category', name='store_category'),
  url(r'^(?P<store_slug>\w+)/search/(?P<keyword>[^/]+)/$', 'store_search', name='store_search'),

  # APIs
  url(r'^(?P<store_slug>\w+)/category/(?P<category_id>\d+)/items/(?P<page>\d*)$', 'store_items', name='store_category_items'),
  url(r'^(?P<store_slug>\w+)/search/(?P<keyword>[^/]+)/items/(?P<page>\d*)$', 'store_items', name='store_search_items'),
  url(r'^(?P<store_slug>\w+)/popular/items/(?P<page>\d*)', 'store_popular_items', name='store_popular_items'),
  url(r'^(?P<store_slug>\w+)/onsale/items/(?P<page>\d*)', 'store_onsale_items', name='store_onsale_items'),
  url(r'^(?P<store_slug>\w+)/featured/(?P<featured_in>\w+)/items/(?P<page>\d*)', 'store_featured_items', name='store_featured_items'),
)
