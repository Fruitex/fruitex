from django.conf.urls import patterns, url

urlpatterns = patterns('page.views',
  # Views
  url(r'^home/$', 'home', name='home'),

  # API
)
