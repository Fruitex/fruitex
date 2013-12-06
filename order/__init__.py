# Paypal setup
from django.core.mail import EmailMessage
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from paypal.standard.ipn.signals import payment_was_successful
from paypal.standard.ipn.signals import payment_was_flagged

from threading import Thread

from order.models import Invoice, Order
from config.email import EMAIL_HOST_USER

def send_receipt(to, invoice_num):
  html_content = loader.render_to_string('reply.html',{'invoice':invoice_num})
  msg = EmailMessage('[Fruitex] Payment of your order %s received.' % invoice_num,html_content,EMAIL_HOST_USER,[to])
  msg.content_subtype = "html"
  msg.send()
def send_receipt_async(to, invoice_num):
  Thread(target=lambda:send_receipt(to, invoice_num)).start()


def send_warning(payer, invoice_num):
  msg = EmailMessage('[Fruitex] Received unexpected payment from %s' % payer, 'invoice: ' % invoice_num, EMAIL_HOST_USER, ['admin@fruitex.ca'])
  msg.content_subtype = 'text'
  msg.send()
def send_warning_async(payer, invoice):
  Thread(target=lambda:send_warning(payer,invoice)).start()


def handle_payment_received(status, ipn):
  invoice_num = ipn.invoice

  # Fetch order
  try:
    invoice = Invoice.objects.get(invoice_num=invoice_num)
  except ObjectDoesNotExist:
    send_warning_async(ipn.payer_email, invoice_num)
    return

  # Invalidate coupon
  coupon = invoice.coupon
  if coupon is not None:
    coupon.used=True
    coupon.save()

  # Update order
  invoice.status=status
  invoice.payer=ipn.payer_email
  invoice.save()

  # Update items
  for order in invoice.orders.all():
    order.status = Order.STATUS_WAITING
    for order_item in order.order_items.all():
      order_item.item.sold_number += order_item.quantity;
      order_item.item.save()

  # Send receipt
  send_receipt_async(invoice.email, invoice_num)

def payment_successful(sender, **kwargs):
  handle_payment_received(Invoice.STATUS_PAID, sender)

def payment_flagged(sender, **kwargs):
  handle_payment_received(Invoice.STATUS_FLAGGED, sender)

payment_was_successful.connect(payment_successful)
payment_was_flagged.connect(payment_flagged)
