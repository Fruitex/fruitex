from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import make_aware, get_default_timezone

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
    # Convert date into the ZERO o'clock of the date with default timezone
    date = make_aware(datetime.datetime(date.year, date.month, date.day), get_default_timezone())

    # Calculate start and end time
    option_start_time = date + datetime.timedelta(minutes=option.start_time)
    option_end_time = option_start_time + datetime.timedelta(minutes=option.time_interval)
    option_store = option.store

    # Find or create the window
    windows = self.filter(start=option_start_time, end=option_end_time,store=option_store)
    if windows.exists():
      return windows[0]
    return self.create(store = option_store,start=option_start_time,end=option_end_time)
