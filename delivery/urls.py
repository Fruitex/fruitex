from django.conf.urls import patterns, url

urlpatterns = patterns('delivery.views',
  # Views
  url(r'^summary/$', 'summary', name='summary'),
)
