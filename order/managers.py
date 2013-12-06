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


class DeliveryWindowManager(models.Manager):
  def get_window(self, option, date):
    for window in DeliveryWindow.objects.all():
      if option.store == window.store and window.date == date:
        if window.start_time <= option.start_time and window.start_time + window.time_interval > option.start_time:
          return window
    window = self.create(store = option.store, date = date, start_time = option.start_time, time_interval = option.time_interval)
    return window
