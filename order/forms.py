from django import forms
from django.core.validators import RegexValidator

from order.models import Payment

# Checkout form definition

class CheckoutForm(forms.Form):
  name = forms.CharField(max_length=64, validators=[
    RegexValidator(regex=r'^[a-zA-Z ]+$'),
  ])
  phone = forms.CharField(max_length=16, validators=[
    RegexValidator(regex=r'^(\+1){0,1}\({0,1}\d{3}[ -\)]{0,1}\d{3}[ -]{0,1}\d{4}$'),
  ])
  email = forms.EmailField()
  address = forms.CharField(min_length=8)
  postcode = forms.CharField(max_length=8, validators=[
    RegexValidator(regex=r'^[a-zA-Z]\d[a-zA-Z] {0,1}\d[a-zA-Z]\d$'),
  ])
  comment = forms.CharField(required=False, widget=forms.Textarea)
  payment_method = forms.ChoiceField(choices=Payment.METHODS, widget=forms.RadioSelect(), initial=Payment.METHODS_PAYPAL)
