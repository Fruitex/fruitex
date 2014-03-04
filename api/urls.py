from django.conf.urls import patterns, include, url
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
# Shop
router.register(r'stores', views.StoreViewSet)
router.register(r'store_customizations', views.StoreCustomizationViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'items', views.ItemViewSet)
# Order
router.register(r'orders', views.OrderViewSet)
router.register(r'order_items', views.OrderItemViewSet)
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'delivery_windows', views.DeliveryWindowViewSet)
router.register(r'coupons', views.CouponViewSet)

urlpatterns = router.urls
