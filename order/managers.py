from django.db import models
from django.core.exceptions import ObjectDoesNotExist

import datetime
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
    option_start_time = datetime.datetime(date.year, date.month, date.day, 0, 0) + datetime.timedelta(minutes=option.start_time)
    option_end_time = option_start_time + datetime.timedelta(minutes=option.time_interval)
    option_store = option.store
    windows = self.filter(start=option_start_time, end=option_end_time,store=option_store)
    if windows.count() > 0:
      return windows[0]
    window = self.create(store = option_store,start=option_start_time,end=option_end_time)

    return window
