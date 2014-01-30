from django.conf.urls import patterns, url

urlpatterns = patterns('order.views',
  # Views
  url(r'^cart/$', 'view_cart', name='cart'),
  url(r'^checkout/$', 'checkout', name='checkout'),
  url(r'^invoice/(?P<id>\d+)/$', 'show_invoice', name='show'),

  # API
  url(r'^coupon/(?P<code>[\w\d-]*)/$', 'coupon', name='coupon')
)
