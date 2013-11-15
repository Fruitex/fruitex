import sys
import os
import django.core.handlers.wsgi

sys.path.append('/fruitex')
sys.path.append('/usr/local/lib/python2.7/site-packages/django')

os.environ['DJANGO_SETTINGS_MODULE']='config.settings'

application = django.core.handlers.wsgi.WSGIHandler()


