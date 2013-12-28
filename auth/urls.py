"""
URLConf for Django user registration and authentication.

Recommended usage is a call to ``include()`` in your project's root
URLConf to include this URLConf for any URL beginning with
``/accounts/``.

"""


from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls as auth_urls
from django.conf.urls import patterns, url, include


from auth.views import activate, register, profile, profile_change


urlpatterns = patterns('',
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           activate,
                           name='activate'),
                       url(r'^register/$',
                           register,
                           name='registration_register'),
                       url(r'^register/complete/$',
                           TemplateView.as_view(template_name='registration/registration_complete.html'),
                           name="register_complete"),
                       url(r'^profile/$',
                           profile,
                           name='profile'),
                       url(r'^change/$',
                           profile_change,
                           name='profile_change'),
                       )

urlpatterns += auth_urls.urlpatterns