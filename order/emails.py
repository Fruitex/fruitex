from django.core.mail import EmailMessage
from django.template import loader
from django.contrib.sites.models import Site
from django.conf import settings

from threading import Thread

def send_payment_received(invoice):
  Thread(target=lambda:send_payment_received_worker(invoice)).start()
def send_payment_received_worker(invoice):
  current_site = Site.objects.get_current()
  html_content = loader.render_to_string('order/payment_received_email.html',{
    'site': current_site,
    'invoice': invoice,
  })
  msg = EmailMessage('[Fruitex] Payment of your order received.', html_content, settings.DEFAULT_FROM_EMAIL, [invoice.email])
  msg.content_subtype = "html"
  msg.send()
