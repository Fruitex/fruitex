from django.conf import settings

import os
import json

import paypalrestsdk
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

def create_raw_payment_for_invoice(invoice, options):
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

def get_redirect_url(raw_payment, default=None):
  raw_payment = json.loads(raw_payment)
  return reduce(lambda x, y: y['href'] if y['rel'] == 'approval_url' else x, raw_payment['links'], default)

def execute_payment(raw_payment, payer_id):
  raw_payment = json.loads(raw_payment)
  payment_id = raw_payment.get('id')
  if payment_id is None or payer_id is None:
    return False

  payment = Payment.find(payment_id)
  result = payment.execute({
    'payer_id': payer_id,
  })
  return result

