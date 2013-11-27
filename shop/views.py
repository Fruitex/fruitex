from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from shop.models import Store, Category, Item, ItemMeta

ITEM_PER_PAGE = 12

# Common operations

def empty_response():
  return HttpResponse('[]', mimetype='application/json')

def common_context(store_slug):
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

  return context

# Views

@csrf_exempt
def to_default(request):
  return HttpResponseRedirect('sobeys');

@csrf_exempt
def store_home(request, store_slug):
  template = loader.get_template('shop/store_home.html')
  context = common_context(store_slug)
  return HttpResponse(template.render(context))

@csrf_exempt
def store_category(request, store_slug, category_id=None):
  template = loader.get_template('shop/store_search.html')
  context = common_context(store_slug)

  # Fetch category for current selection
  if category_id is not None:
    try:
      category = Category.objects.get(id=category_id)
      context['category'] = category
    except ObjectDoesNotExist:
      pass

  return HttpResponse(template.render(context))

# APIs

@csrf_exempt
def store_items(request, store_slug, category_id=None, page=1):
  # Fetch category for current selection
  if category_id is None:
    return empty_response()
  else:
    try:
      category = Category.objects.get(id=category_id)
    except ObjectDoesNotExist:
      return empty_response()

  items = category.items.order_by('name')
  if len(page) > 0:
    page = int(page)
    items = items[ITEM_PER_PAGE * (page - 1) : ITEM_PER_PAGE * page]

  return HttpResponse(serializers.serialize('json', items), mimetype='application/json')
