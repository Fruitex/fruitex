from django.conf.urls import patterns, url

urlpatterns = patterns('shop.views',
  url(r'^$', 'toDefault', name='toDefault'),
  url(r'^(?P<store_slug>\w*)/$', 'storeHome', name='storeHome'),
  # url(r'^getItems$', views.getItems),
  # url(r'^getPopularItems$', views.getPopularItems),
  # url(r'^getOnSaleItems$', views.getOnSaleItems),
  # url(r'^computeSummary$', views.computeSummary),
)
