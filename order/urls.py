from django.conf.urls import patterns, url, include

urlpatterns = patterns('order.views',
  # Views
  url(r'^cart/$', 'view_cart', name='cart'),
  url(r'^new/$', 'new_order', name='new'),
  url(r'^paypal-ipn/', include('paypal.standard.ipn.urls'), name='paypal-ipn'),
)
