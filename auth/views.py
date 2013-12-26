"""
Views which allow users to create and activate accounts.

"""


from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from auth.form import RegistrationForm, ProfileForm
from auth.models import RegistrationProfile, UserProfile
from auth.auth_settings import ACCOUNT_SETTING



def activate(request, activation_key,
             template_name='registration/activate.html',
             extra_context=None):
    """
    Activate a ``User``'s account, if their key is valid and hasn't
    expired.
    
    By default, uses the template ``registration/activate.html``; to
    change this, pass the name of a template as the keyword argument
    ``template_name``.
    
    **Context:**
    
    account
        The ``User`` object corresponding to the account, if the
        activation was successful. ``False`` if the activation was not
        successful.
    
    expiration_days
        The number of days for which activation keys stay valid after
        registration.
    
    Any values passed in the keyword argument ``extra_context`` (which
    must be a dictionary) will be added to the context as well; any
    values in ``extra_context`` which are callable will be called
    prior to being added to the context.

    **Template:**
    
    registration/activate.html or ``template_name`` keyword argument.
    
    """
    activation_key = activation_key.lower() # Normalize before trying anything with it.
    account = RegistrationProfile.objects.activate_user(activation_key)
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'account': account,
                                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS },
                              context_instance=context)


def register(request, success_url='/accounts/register/complete/',
             form_class=RegistrationForm, profile_callback=None,
             template_name='registration/registration_form.html',
             extra_context=None):
    """
    Allow a new user to register an account.
    
    Following successful registration, redirects to either
    ``/accounts/register/complete/`` or, if supplied, the URL
    specified in the keyword argument ``success_url``.
    
    By default, ``registration.forms.RegistrationForm`` will be used
    as the registration form; to change this, pass a different form
    class as the ``form_class`` keyword argument. The form class you
    specify must have a method ``save`` which will create and return
    the new ``User``, and that method must accept the keyword argument
    ``profile_callback`` (see below).
    
    To enable creation of a site-specific user profile object for the
    new user, pass a function which will create the profile object as
    the keyword argument ``profile_callback``. See
    ``RegistrationManager.create_inactive_user`` in the file
    ``models.py`` for details on how to write this function.
    
    By default, uses the template
    ``registration/registration_form.html``; to change this, pass the
    name of a template as the keyword argument ``template_name``.
    
    **Context:**
    
    form
        The registration form.
    
    Any values passed in the keyword argument ``extra_context`` (which
    must be a dictionary) will be added to the context as well; any
    values in ``extra_context`` which are callable will be called
    prior to being added to the context.

    **Template:**
    
    registration/registration_form.html or ``template_name`` keyword
    argument.
    
    """
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save(profile_callback=profile_callback)
            if ACCOUNT_SETTING.NEED_ACTIVATION:
                return HttpResponseRedirect('/accounts/register/complete/')
            else:
                return HttpResponseRedirect('/accounts/login')
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)


class LoginRequiredMixin(object):
    """Ensures that the user is authenticated in order to access the view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        profile = user.get_profile()
        return {
            'user': user.username,
            'firstname': user.first_name,
            'lastname': user.last_name,
            'email': user.email,
            'phonenum': profile.phone_num,
            'address': profile.address
        }

profile = ProfileView.as_view()


class ProfileChangeView(LoginRequiredMixin, FormView):
    form_class = ProfileForm
    template_name = 'registration/profile_change.html'

    def get_form_kwargs(self):
        kwargs = super(ProfileChangeView, self).get_form_kwargs()
        kwargs['instance'] = UserProfile.objects.get(
            user=self.request.user)
        user = self.request.user
        profile = user.get_profile()
        kwargs['initial'].update({
            'firstname': user.first_name,
            'lastname': user.last_name,
            'email': user.email,
            'address': profile.address,
            'phonenum': profile.phone_num,
        })
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _(u'Profile changed'))
        return redirect('/accounts/profile')

profile_change = ProfileChangeView.as_view()
