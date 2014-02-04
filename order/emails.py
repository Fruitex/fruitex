from django.core.mail import EmailMessage
from django.template import loader
from django.contrib.sites.models import Site
from django.conf import settings

from threading import Thread

def send_msg_async(msg):
  Thread(target=lambda:msg.send()).start()

def send_invoice_email(invoice, template, subject):
  current_site = Site.objects.get_current()
  html_content = loader.render_to_string(template,{
    'site': current_site,
    'invoice': invoice,
  })
  msg = EmailMessage(subject, html_content, settings.DEFAULT_FROM_EMAIL, [invoice.email])
  msg.content_subtype = "html"
  send_msg_async(msg)

def send_order_received(invoice):
  send_invoice_email(
    invoice,
    'order/order_received_email.html',
    '[Fruitex] Your order is being processed (#%s)' % invoice.invoice_num
  )
