from django.conf import settings

import paypalrestsdk
import os

from paypalrestsdk import Payment

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

def create_payment_for_invoice(invoice, options):
  return_url = options.get('return_url')
  cancel_url = options.get('cancel_url')

  description = 'Fruitex Invoice #' + str(invoice.id)
  payment = Payment({
    'intent': 'sale',
    'payer': {
      'payment_method': 'paypal',
    },
    'transactions': [{
      'amount': {
        'total': str(invoice.total),
        'currency': 'CAD',
        'details': {
          'subtotal': str(invoice.subtotal - invoice.discount),
          'tax': str(invoice.tax),
          'shipping': str(invoice.delivery),
        },
      },
      'description': description,
    }],
    'redirect_urls': {
      'return_url': return_url,
      'cancel_url': cancel_url,
    }
  })

  if not payment.create():
    return None

  return payment
