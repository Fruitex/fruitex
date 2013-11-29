from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Statics
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.BASE_DIR + 'static', 'show_indexes': True}),

    # Apps
    url(r'^$', 'fruitex.views.home', name='home'),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    url(r'^order/', include('order.urls', namespace='order')),

    # Dango admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Accounts
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',name="my_login"),

    # Pages
    url(r'^error', 'fruitex.views.error'),
    url(r'^not-support', 'fruitex.views.browserNotSupport'),
)
