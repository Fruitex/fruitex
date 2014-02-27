from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

# API
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'stores', views.StoreViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order_items', views.OrderItemViewSet)
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'delivery_windows', views.DeliveryWindowViewSet)

urlpatterns = patterns('',
    # Statics
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.BASE_DIR + 'static', 'show_indexes': True}),

    # Apps
    url(r'^$', 'page.views.home', name='home'),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    url(r'^order/', include('order.urls', namespace='order')),
    url(r'^delivery/', include('delivery.urls', namespace='delivery')),
    url(r'^page/', include('page.urls', namespace='page')),

    # Django admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Accounts
    url(r'^account/', include('account.urls')),

    # API
    url(r'^api/', include(router.urls)),

    # Pages
    url(r'^error', 'fruitex.views.error'),
    url(r'^not-support', 'fruitex.views.browserNotSupport'),
)
