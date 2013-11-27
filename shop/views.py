from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from shop.models import Store, Category, Item, ItemMeta

ITEM_PER_PAGE = 12
POPULAR_ITEM_PER_PAGE = 8
ON_SALE_ITEM_PER_PAGE = 4

# Common operations

def empty_response():
  return HttpResponse('[]', mimetype='application/json')

def json_response(queryset):
  return HttpResponse(serializers.serialize('json', queryset), mimetype='application/json')

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

def limit_to_page(queryset, page=1, per_page=ITEM_PER_PAGE):
  if type(page) is not int:
    try:
      page = int(page)
    except ValueError:
      page = 1
  return queryset[per_page * (page - 1) : per_page * page]

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
  items = Item.objects.order_by('name')
  if category_id is not None and len(category_id) > 0:
    items = items.filter(category__id=category_id)
  items = limit_to_page(items, page, ITEM_PER_PAGE)

  return json_response(items)

@csrf_exempt
def store_popular_items(request, store_slug, page=1):
  items = Item.objects.order_by('-sold_number')
  items = limit_to_page(items, page, POPULAR_ITEM_PER_PAGE)

  return json_response(items)

@csrf_exempt
def store_onsale_items(request, store_slug, page=1):
  items = Item.objects.filter(on_sale=True).order_by('-sold_number')
  items = limit_to_page(items, page, ON_SALE_ITEM_PER_PAGE)

  return json_response(items)
