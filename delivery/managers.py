from django.db import models

class DeliveryBucketManager(models.Manager):
  def create_bucket_from_window(self, window, driver):
    return self.create(start = window.start, end = window.end, driver = driver)
