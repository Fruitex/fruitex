from django.conf.urls import patterns, url

urlpatterns = patterns('order.views',
  # Views
  url(r'^cart/$', 'view_cart', name='cart'),
  url(r'^checkout/$', 'checkout', name='checkout'),
  url(r'^invoice/(?P<id>\d+)/$', 'show_invoice', name='show'),

  # PayPal
  url(r'^payment/paypal/execute/(?P<id>\d+)$', 'payment_paypal_execute', name='payment_paypal_execute'),
  url(r'^payment/paypal/cancel/(?P<id>\d+)$', 'payment_paypal_cancel', name='payment_paypal_cancel'),

  # API
  url(r'^coupon/(?P<code>[\w\d-]*)/$', 'coupon', name='coupon')
)
