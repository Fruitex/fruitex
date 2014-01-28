from django.conf import settings

import paypalrestsdk
import os

def bootstrap():
  # Config Paypal
  try:
    # Check environment var exists
    os.environ['PAYPAL_MODE']
    os.environ['PAYPAL_CLIENT_ID']
    os.environ['PAYPAL_CLIENT_SECRET']
  except:
    # Config with settings if no env var specified
    paypalrestsdk.configure(settings.PAYPAL_CONFIG)
