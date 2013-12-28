from django.http import HttpResponse
from django.template import Context, loader
from django.utils.timezone import make_aware, get_default_timezone

from datetime import datetime, timedelta

from shop.models import Store

def home(request):
  stores = Store.objects.all()

  context = Context({
    'stores': stores,
  })

  template = loader.get_template('page/home.html')
  return HttpResponse(template.render(context))
