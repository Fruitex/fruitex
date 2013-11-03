from django.conf.urls import patterns, include, url
from django.conf import settings
import config
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fruitex.views.home', name='home'),
    # url(r'^fruitex/', include('fruitex.foo.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': config.BASE_DIR + 'static', 'show_indexes': True}),
    url(r'^$', 'fruitex.views.home', name='home'),
    url(r'^home/', include('home.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^orders/', 'fruitex.views.orders'),
    url(r'^delivered', 'fruitex.views.delivered'),
    url(r'^norders/', 'fruitex.views.norders'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',name="my_login"),

    url(r'^fruitex-magic-ipn/', include('paypal.standard.ipn.urls')),
    url(r'^redir/', 'fruitex.views.redir'),
    url(r'^check_order/', 'fruitex.views.check_order'),
    url(r'^error', 'fruitex.views.error'),
    url(r'^return_page', 'fruitex.views.return_page'),
    url(r'^not-support', 'fruitex.views.browserNotSupport'),
    url(r'^get_orders', 'fruitex.views.get_orders'),
    url(r'^group_orders', 'fruitex.views.group_orders'),
)
