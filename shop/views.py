from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from shop.models import Store, Category, Item

ITEM_PER_PAGE = 12
POPULAR_ITEM_PER_PAGE = 8
ON_SALE_ITEM_PER_PAGE = 4
FEATURED_ITEM_PER_PAGE = 4

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

def items_for_store(store_slug):
  return Item.objects.filter(category__store__slug=store_slug)

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

def store_home(request, store_slug):
  template = loader.get_template('shop/store_home.html')
  context = common_context(store_slug)
  return HttpResponse(template.render(context))

def store_category(request, store_slug, category_id=None):
  template = loader.get_template('shop/store_search.html')
  context = common_context(store_slug)

  # Fetch category for current selection
  if category_id is not None:
    try:
      category = Category.objects.get(id=category_id)
      context['category'] = category
    except ObjectDoesNotExist:
      return store_home(request, store_slug)

  return HttpResponse(template.render(context))

def store_search(request, store_slug, keyword=None):
  template = loader.get_template('shop/store_search.html')
  context = common_context(store_slug)

  # Add search_keyword to the context
  if keyword is not None:
    context['search_keyword'] = keyword

  return HttpResponse(template.render(context))

# APIs

def store_items(request, store_slug, category_id=None, keyword=None, page=1):
  items = items_for_store(store_slug).order_by('name')
  if category_id is not None and len(category_id) > 0:
    items = items.filter(category__id=category_id)
  if keyword is not None and len(keyword) > 0:
    items = items.filter(name__contains=keyword)
  items = limit_to_page(items, page, ITEM_PER_PAGE)

  return json_response(items)

def store_popular_items(request, store_slug, page=1):
  items = items_for_store(store_slug).order_by('-sold_number')
  items = limit_to_page(items, page, POPULAR_ITEM_PER_PAGE)

  return json_response(items)

def store_onsale_items(request, store_slug, page=1):
  items = items_for_store(store_slug).filter(on_sale=True).order_by('-sold_number')
  items = limit_to_page(items, page, ON_SALE_ITEM_PER_PAGE)

  return json_response(items)

def store_featured_items(request, store_slug, featured_in, page=1):
  items = items_for_store(store_slug).filter(featured=featured_in).order_by('name')
  items = limit_to_page(items, page, FEATURED_ITEM_PER_PAGE)

  return json_response(items)
