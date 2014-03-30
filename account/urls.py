"""
URLConf for Django user registration and authentication.

Recommended usage is a call to ``include()`` in your project's root
URLConf to include this URLConf for any URL beginning with
``/accounts/``.

"""

from django.views.generic import TemplateView
from django.contrib.auth import urls as auth_urls
from django.conf.urls import patterns, url


urlpatterns = patterns('account.views',
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^activate/(?P<activation_key>\w+)/$',
       'activate',
       name='activate'),
    url(r'^register/$',
       'register',
       name='registration_register'),
    url(r'^register/complete/$',
       TemplateView.as_view(template_name='registration/registration_complete.html'),
       name="register_complete"),
    url(r'^profile/$',
       'profile',
       name='profile'),
    url(r'^profile/change/$',
       'profile_change',
       name='profile_change'),
    url(r'^invoices/(?P<invoice_num>[\w-]*)$',
      'invoices',
      name='account_invoices'),
)

urlpatterns += auth_urls.urlpatterns
