from django.db import models

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
    time = models.DateTimeField();
    invoice = models.CharField(max_length=30)


from paypal.standard.ipn.signals import payment_was_successful
from paypal.standard.ipn.signals import payment_was_flagged

def payment_successful(sender, **kwargs):
  invoice = sender.invoice
  for o in Order.objects.filter(invoice=invoice):
    o.status="paid"
    o.save()

def payment_flagged(sender, **kwargs):
  invoice = sender.invoice
  for o in Order.objects.filter(invoice=invoice):
    o.status="flagged"
    o.save()

payment_was_successful.connect(payment_successful)
payment_was_flagged.connect(payment_flagged)
