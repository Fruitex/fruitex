"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.mail import send_mail

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
def s_email():
    send_mail('no reply','', 'noreply@fruitex.com',['not-found@qq.com','luregun@gmail.com'], fail_silently=False,html_message='<html><body>Test</body></html>')
