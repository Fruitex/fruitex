from django.core.mail import send_mail
from django.db import models
from django.db.models import F
from home.models import Item
import json
from django.core.mail import EmailMessage
from django.template import loader
from fruitex.settings import EMAIL_HOST_USER

# Create your models here.
class Order(models.Model):
    def __unicode__(self):
        return self.invoice
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    postcode = models.CharField(max_length=10)
    items = models.CharField(max_length=1000)
    price = models.FloatField()
    tax = models.FloatField()
    shipping = models.FloatField()
    status = models.CharField(max_length=20)
    delivery_window = models.CharField(max_length=20)
    time = models.DateTimeField()
    invoice = models.CharField(max_length=30)
    sub_type = models.CharField(max_length=30,default='')
    allow_sub_detail = models.CharField(max_length=2000)
    email = models.CharField(max_length=64)

class Coupon(models.Model):
  def __unicode__(self):
    return self.code
  code = models.CharField(max_length=30)
  value = models.FloatField()
  used = models.BooleanField()


from paypal.standard.ipn.signals import payment_was_successful
from paypal.standard.ipn.signals import payment_was_flagged
from threading import Thread

def send_receipt(to, invoice):
  Thread(target=lambda:send_html_message(to,invoice)).start()

def handle_payment_received(status, ipn):
  invoice = ipn.invoice
  coupon = json.loads(ipn.custom)['coupon']
  #invalidate coupon
  Coupon.objects.filter(code=coupon).update(used=True)
  order = Order.objects.filter(invoice=invoice)[0]
  order.status=status
  order.email=ipn.payer_email
  order.save()
  ids = json.loads(order.items)
  for it in Item.objects.filter(id__in=set(ids)):
    it.sold_number=it.sold_number + ids.count(it.id)
    it.save()
  send_receipt(ipn.payer_email,invoice)

def payment_successful(sender, **kwargs):
  handle_payment_received('paid', sender)

def payment_flagged(sender, **kwargs):
  handle_payment_received('flagged', sender)

payment_was_successful.connect(payment_successful)
payment_was_flagged.connect(payment_flagged)

def send_html_message(to,invoice):
    html_content = loader.render_to_string('reply.html',{'invoice':invoice})
    msg = EmailMessage('[Fruitex] Payment of your order %s received.' % invoice,html_content,EMAIL_HOST_USER,[to])
    msg.content_subtype = "html"
    msg.send()