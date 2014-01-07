from django.http import HttpResponse
from django.template import Context, loader

from shop.models import Store

def home(request):
  stores = Store.objects.order_by('id')[:5]

  context = Context({
    'stores': stores,
  })

  template = loader.get_template('page/home.html')
  return HttpResponse(template.render(context))
