from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from order.models import Coupon

# Checkout form definition

class CheckoutForm(forms.Form):
  def _validate_coupon_code(coupon_code):
    coupon = Coupon.objects.get_valid_coupon(coupon_code)
    if coupon == False:
      raise ValidationError(u'%s is not a valid coupon' % coupon_code)

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
  coupon_code = forms.CharField(required=False, validators=[_validate_coupon_code])
