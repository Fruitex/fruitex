from django.test import TestCase
from datetime import date
from shop.models import Store, DeliveryOption
from order.models import DeliveryWindow


class SimpleTest(TestCase):  
  def test_basic_addition(self):  
    store1 = Store.objects.create(name='UW')
    store2 = Store.objects.create(name='UT')
    option1 = DeliveryOption(store=store1,start_time=60,time_interval=120)
    option2 = DeliveryOption(store=store1,start_time=60,time_interval=60)
    option3 = DeliveryOption(store=store2,start_time=60,time_interval=120)
    option4 = DeliveryOption(store=store2,start_time=60,time_interval=60)
    DeliveryWindow.objects.get_window(option1, date(2000, 1, 1))
    self.assertEqual(DeliveryWindow.objects.count(), 1)
    DeliveryWindow.objects.get_window(option1, date(2000, 1, 1))
    self.assertEqual(DeliveryWindow.objects.count(), 1)
    DeliveryWindow.objects.get_window(option3, date(2000, 1, 1))
    self.assertEqual(DeliveryWindow.objects.count(), 2)
    DeliveryWindow.objects.get_window(option3, date(2000, 1, 2))
    self.assertEqual(DeliveryWindow.objects.count(), 3)
    DeliveryWindow.objects.get_window(option2, date(2000, 1, 1))
    DeliveryWindow.objects.get_window(option4, date(2000, 1, 1))
    self.assertEqual(DeliveryWindow.objects.count(), 5)
    print option1
    print DeliveryWindow.objects.all()[0]
