# Paypal setup
from django.core.mail import EmailMessage
from django.template import loader
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from paypal.standard.ipn.signals import payment_was_successful
from paypal.standard.ipn.signals import payment_was_flagged

from threading import Thread

from order.models import Invoice, Order

def send_receipt(to, invoice):
  html_content = loader.render_to_string('email/reply.html',{
    'invoice': invoice,
    'order_url': 'http://' + settings.DOMAIN + reverse('order:show', kwargs={'id': invoice.id}),
  })
  msg = EmailMessage('[Fruitex] Payment of your order %s received.' % invoice.invoice_num, html_content, settings.EMAIL_HOST_USER, [to])
  msg.content_subtype = "html"
  msg.send()
def send_receipt_async(to, invoice):
  Thread(target=lambda:send_receipt(to, invoice)).start()


def send_warning(payer, invoice_num):
  msg = EmailMessage('[Fruitex] Received unexpected payment from %s' % payer, 'invoice: ' % invoice_num, settings.EMAIL_HOST_USER, ['admin@fruitex.ca'])
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
    for order_item in order.order_items.all():
      order_item.item.sold_number += order_item.quantity;
      order_item.item.save()
    order.status = Order.STATUS_WAITING
    order.save()

  # Send receipt
  send_receipt_async(invoice.email, invoice)

def payment_successful(sender, **kwargs):
  handle_payment_received(Invoice.STATUS_PAID, sender)

def payment_flagged(sender, **kwargs):
  handle_payment_received(Invoice.STATUS_FLAGGED, sender)

payment_was_successful.connect(payment_successful)
payment_was_flagged.connect(payment_flagged)
