from rest_framework import routers
from account.api.views import UserViewSet
from shop.api.views import StoreViewSet, CategoryViewSet, ItemViewSet
from order.api.views import OrderViewSet, InvoiceViewSet, DeliveryWindowViewSet, CouponViewSet
from delivery.api.views import DeliveryBucketViewSet

router = routers.DefaultRouter()
# Account
router.register(r'users', UserViewSet)
# Shop
router.register(r'stores', StoreViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'items', ItemViewSet)
# Order
router.register(r'orders', OrderViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'delivery_windows', DeliveryWindowViewSet)
router.register(r'coupons', CouponViewSet)
# Delivery
router.register(r'delivery_buckets', DeliveryBucketViewSet)

urlpatterns = router.urls
