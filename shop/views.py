from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.exceptions import ObjectDoesNotExist

from shop.models import Store, Category, Item, ItemMeta

# Views

@csrf_exempt
def to_default(request):
  return HttpResponseRedirect('sobeys');

@csrf_exempt
def store_front(request, store_slug, category_id=None):
  template = loader.get_template('shop/store_home.html')

  # Fetch all stores, current store and base categories of current store
  try:
    stores = Store.objects.all();
    store = stores.get(slug=store_slug);
    categories = store.categories.filter(parent__isnull=True)
  except ObjectDoesNotExist as e:
    return HttpResponse(e)

  # Build common context
  context = Context({
    'stores': stores,
    'store':store,
    'categories':categories,
  })

  # Fetch category for current selection
  if category_id is not None:
    try:
      category = Category.objects.get(id=category_id)
      context['category'] = category
    except ObjectDoesNotExist:
      pass

  return HttpResponse(template.render(context))
