from django.http import HttpResponse
from django.template import Context, loader
from django.utils.timezone import make_aware, get_default_timezone

from datetime import datetime, timedelta

from order.models import DeliveryWindow

def summary(request):
  datetime_threshold = make_aware(datetime.now() - timedelta(days=30), get_default_timezone())
  delivery_windows = DeliveryWindow.objects.filter(start__gt=datetime_threshold)

  context = Context({
    'delivery_windows': delivery_windows,
  })

  template = loader.get_template('delivery/summary.html')
  return HttpResponse(template.render(context))

