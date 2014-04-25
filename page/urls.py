from django.conf.urls import patterns, url

urlpatterns = patterns('page.views',
  # Views
  url(r'^home/$', 'home', name='home'),
  url(r'^faq/$', 'faq', name='faq'),
  url(r'^privacy/$', 'privacy', name='privacy')

  # API
)
