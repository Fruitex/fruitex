from django.conf.urls import patterns, url

urlpatterns = patterns('delivery.views',
  # Views
  url(r'^summary/$', 'summary', name='summary'),
  url(r'^detail/(?P<id>\d+)/$', 'detail', name='detail'),
  url(r'^summary/invoices/(?P<ids>\d+(\+\d+)*)/$', 'invoices', name='invoices')

  # API
)
