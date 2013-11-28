# Paypal setup
from django.core.mail import EmailMessage
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from paypal.standard.ipn.signals import payment_was_successful
from paypal.standard.ipn.signals import payment_was_flagged

from threading import Thread
import json

from home.models import Item
from order.models import Order, OrderItem, Coupon
from config.email import EMAIL_HOST_USER

def send_receipt(to, invoice):
  html_content = loader.render_to_string('reply.html',{'invoice':invoice})
  msg = EmailMessage('[Fruitex] Payment of your order %s received.' % invoice,html_content,EMAIL_HOST_USER,[to])
  msg.content_subtype = "html"
  msg.send()
def send_receipt_async(to, invoice):
  Thread(target=lambda:send_receipt(to,invoice)).start()


def send_warning(payer, invoice):
  msg = EmailMessage('[Fruitex] Received unexpected payment from %s' % payer, 'invoice: ' % invoice, EMAIL_HOST_USER, ['admin@fruitex.ca'])
  msg.content_subtype = 'text'
  msg.send()
def send_warning_async(payer, invoice):
  Thread(target=lambda:send_warning(payer,invoice)).start()


def handle_payment_received(status, ipn):
  invoice = ipn.invoice
  coupon = json.loads(ipn.custom)['coupon']
  # Invalidate coupon
  Coupon.objects.filter(code=coupon).update(used=True)

  # Fetch order
  try:
    order = Order.objects.get(invoice=invoice)
  except ObjectDoesNotExist:
    send_warning_async(ipn.payer_email, invoice)
    return

  # Update order
  order.status=status
  order.email=ipn.payer_email
  order.save()

  # Update items
  for order_item in OrderItem.filter(order__id=order.id):
    order_item.item.sold_number += order_item.quantity;
    order_item.item.save()

  # Send receipt
  send_receipt_async(ipn.payer_email,invoice)

def payment_successful(sender, **kwargs):
  handle_payment_received(Order.STATUS_PAID, sender)

def payment_flagged(sender, **kwargs):
  handle_payment_received(Order.STATUS_FLAGGED, sender)

payment_was_successful.connect(payment_successful)
payment_was_flagged.connect(payment_flagged)
