from django.conf.urls import patterns, url, include

from drf_toolbox import routers
from account.api.views import UserViewSet
from shop.api.views import StoreViewSet, CategoryViewSet, ItemViewSet
from order.api.views import OrderViewSet, InvoiceViewSet, DeliveryWindowViewSet
from delivery.api.views import DeliveryBucketViewSet

router = routers.Router()
# Account
router.register(r'users', UserViewSet)
# Shop
router.register(r'stores', StoreViewSet)
router.register(r'stores/categories', CategoryViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'categories/items', ItemViewSet)
router.register(r'items', ItemViewSet)
# Order
router.register(r'orders', OrderViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'delivery_windows', DeliveryWindowViewSet)
# Delivery
router.register(r'delivery_buckets', DeliveryBucketViewSet)

urlpatterns = patterns('',
  url(r'', include(router.urls)),
  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
