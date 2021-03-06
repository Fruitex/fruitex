from django.conf.urls import patterns, url, include

from drf_toolbox import routers
from account.api.views import UserViewSet, CurrentUserView, CurrentUserInvoicesView, CurrentUserDeliveryBucketsView
from shop.api.views import StoreViewSet, CategoryViewSet, ItemViewSet
from order.api.views import InvoiceViewSet, OrderViewSet, OrderItemViewSet, DeliveryWindowViewSet
from delivery.api.views import DeliveryBucketViewSet, DeliveryBucketOrderViewSet

# General resources
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
router.register(r'invoices', InvoiceViewSet)
router.register(r'invoices/orders', OrderViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'orders/order_items', OrderItemViewSet)
router.register(r'order_items', OrderItemViewSet)
router.register(r'delivery_windows', DeliveryWindowViewSet)
# Delivery
router.register(r'delivery_buckets', DeliveryBucketViewSet)
router.register(r'delivery_buckets/orders', DeliveryBucketOrderViewSet)


# Current user resources
user_urlpatterns = patterns('',
  url(r'^$', CurrentUserView.as_view()),
  url(r'^invoices/$', CurrentUserInvoicesView.as_view()),
  url(r'^delivery_buckets/$', CurrentUserDeliveryBucketsView.as_view()),
)

# Expose
urlpatterns = patterns('',
  url(r'^', include(router.urls)),
  url(r'^users/current/', include(user_urlpatterns)),
  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
