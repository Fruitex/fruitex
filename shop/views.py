from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.exceptions import ObjectDoesNotExist

from shop.models import Store, Category, Item, ItemMeta

@csrf_exempt
def toDefault(request):
  return HttpResponseRedirect('sobeys');

@csrf_exempt
def storeHome(request, store_slug=''):
  template = loader.get_template('shop/store_home.html')
  try:
    stores = Store.objects.all();
    store = stores.get(slug=store_slug);
    categories = store.categories.filter(parent__isnull=True)
  except ObjectDoesNotExist as e:
    return HttpResponse(e)
  context = Context({
    'stores': stores,
    'store':store,
    'categories':categories,
  })

  return HttpResponse(template.render(context))
