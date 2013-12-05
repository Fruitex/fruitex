from django.conf.urls import patterns, url, include

urlpatterns = patterns('order.views',
  # Views
  url(r'^cart/$', 'view_cart', name='cart'),
  url(r'^invoice/(?P<id>\d+)/$', 'show_invoice', name='show'),
  url(r'^new/$', 'new_from_cart', name='new'),
  url(r'^paypal-ipn/$', include('paypal.standard.ipn.urls'), name='paypal-ipn'),

  # API
  url(r'^coupon/(?P<code>[\w\d-]*)/$', 'coupon', name='coupon')
)
