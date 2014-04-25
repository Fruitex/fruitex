from django.http import HttpResponse
from django.template import RequestContext, loader

from shop.models import Store

def home(request):
  stores = Store.objects.order_by('display_order')[:5]

  context = RequestContext(request, {
    'stores': stores,
  })

  template = loader.get_template('page/home.html')
  return HttpResponse(template.render(context))

def faq(request):
  context = RequestContext(request)
  template = loader.get_template('page/faq.html')
  return HttpResponse(template.render(context))

def privacy(request):
  context = RequestContext(request)
  template = loader.get_template('page/privacy.html')
  return HttpResponse(template.render(context))