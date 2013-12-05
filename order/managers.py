from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from datetime import date

class CouponManager(models.Manager):
  def get_valid_coupon(self, coupon_code):
    try:
      coupon = self.get(code=coupon_code)
    except ObjectDoesNotExist:
      return False
    if coupon.expire is not None and date.today() > coupon.expire:
      return False
    if coupon.used:
      return False
    return coupon
