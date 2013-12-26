"""
URLConf for Django user registration and authentication.

Recommended usage is a call to ``include()`` in your project's root
URLConf to include this URLConf for any URL beginning with
``/accounts/``.

"""


from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, url, include

from auth.views import activate, register, profile, profile_change


urlpatterns = patterns('',
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           activate,
                           name='registration_activate'),
                       url(r'^login/$',
                           auth_views.login,
                           {'template_name': 'registration/login.html'},
                           name='auth_login'),
                       url(r'^logout/$',
                           auth_views.logout,
                           {'template_name': 'registration/logout.html'},
                           name='auth_logout'),
                       url(r'^password/change/$', auth_views.password_change,
                           {'template_name': 'registration/password_change.html'},
                            name='auth_password_change'),
                       url(r'^password/change/done/$', auth_views.password_change_done,
                           {'template_name': 'registration/password_change_done.html'},
                           name='auth_password_change_done'),
                       url(r'^password/reset/$', auth_views.password_reset,
                           {'template_name': 'registration/password_reset.html',
                           'email_template_name': 'registration/password_reset_email.html'},
                           name='auth_password_reset'),
                       url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           auth_views.password_reset_confirm,
                           {'template_name': 'registration/password_reset_confirm.html'},
                           name='auth_password_reset_confirm'),
                       url(r'^password/reset/complete/$', auth_views.password_reset_complete,
                           {'template_name': 'registration/password_reset_complete.html'},
                           name='auth_password_reset_complete'),
                       url(r'^password/reset/done/$', auth_views.password_reset_done,
                           {'template_name': 'registration/password_reset_done.html'},
                           name='auth_password_reset_done'),
                       url(r'^register/$',
                           register,
                           name='registration_register'),
                       url(r'^register/complete/$',
                           TemplateView.as_view(template_name='registration/registration_complete.html'),
                           name="home"),
                       url(r'^profile/$',
                           profile,
                           name='profile'),
                       url(r'^change/$',
                           profile_change,
                           name='profile_change'),
                       )
 