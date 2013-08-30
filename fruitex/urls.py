from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fruitex.views.home', name='home'),
    # url(r'^fruitex/', include('fruitex.foo.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/fruitex/static', 'show_indexes': True}),
    url(r'^$', 'fruitex.views.home', name='home'),
    url(r'^home/', include('home.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^orders/', include('orders.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^fruitex-magic-ipn/', include('paypal.standard.ipn.urls')),
    url(r'^redir/', 'fruitex.views.redir'),
    url(r'^check_order/', 'fruitex.views.check_order'),
    url(r'^fruitex-admin', 'fruitex.views.fruitex_admin'),
)
