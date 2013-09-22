from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import Context, loader
from home.models import Store, Item
import json
from category import category
from django.views.decorators.csrf import csrf_exempt
import re
from django.db.models import Q
from django.http import HttpResponseRedirect
from urllib import unquote

TAX_RATE = 0.13

labels = {
    'Produce': 'cate_label_produce.png',
    'Home & Lifestyle': 'cate_label_home.png',
    'Groceries': 'cate_label_grocery.png',
    'Snacks & Candies': 'cate_label_candy.png',
    'Beverages':'cate_label_beverage.png',
    'Pet Care':'cate_label_pet.png',
    'Department A-E': 'cate_label_book.png',
    'Department F-J': 'cate_label_book.png',
    'Department K-O': 'cate_label_book.png',
    'Department P-Z': 'cate_label_book.png',
}

stores = {
    'sobeys':'Sobeys',
    'bookstore':'WLU Bookstore'
}
stores_list = [{'name':'sobeys','description':'Sobeys'},{'name':'bookstore','description':'WLU Bookstore'}]
def getStore(request):
    if 'query' in request.GET:
        stores,_ = extractStore(request.GET['query'])
        if len(stores) > 0 and stores[0] in category:
            return stores[0]
    return 'sobeys'

def getCate(request):
    if 'query' in request.GET:
        cates,_ = extractCate(request.GET['query'])
        if len(cates) > 0:
            return cates[0]
    return ''
def isSearch(request):
    if 'query' in request.GET:
        return not(re.match(r"^store:[^\s]+$",request.GET['query'].strip()))
    return False
def getSearchContent(request):
    if not('query' in request.GET):
        return ''
    query = request.GET['query'].strip()
    if isSearch(request) and not(re.match(r'.*cate:".*',query)):
        search = query = re.findall('store:[^\s]+\s+([^\s]+)',query)
        if search:
            return search[0]
        return ''
    return ''
def getCartSize(request):
    if 'cart' in request.COOKIES:
        try:
            cart_size = len(json.loads(unquote(request.COOKIES['cart']))) 
        except ValueError, e:
            cart_size = 0
        return cart_size
    return 0;

@csrf_exempt
def main(request):
    if not('query' in request.GET):
        return HttpResponseRedirect('/home?query=store:sobeys');
    template = loader.get_template('home/home.html')
    store = getStore(request)
    context = Context({
        'cateNav':getCateNav(category[store]),
        'current_store_description':stores[store],
        'cate':getCate(request),
        'stores':stores_list,
        'current_store_name':store,
        'is_search':isSearch(request),
        'search_content':getSearchContent(request),
        'cart_size':getCartSize(request),
    })
    return HttpResponse(template.render(context))
def getCateNav(cate):
    navs = []
    def getCateNum(c):
        res = 0
        for x in cate[c]:
            res += len(cate[c][x])
        return res
    mck = sorted(cate.keys(),key=getCateNum,reverse=True)
    for k in mck:
        nav = {'k':k,'labels':labels.get(k)}
        cateNum = getCateNum(k)
        if cateNum % 15 == 0:
            colNum = cateNum / 15
            if colNum == 0:
                colNum = 1
        else:
            colNum = cateNum / 15 + 1
        cols = []
        sks = sorted(cate[k].keys())
        for cn in range(colNum):
            col = []
            for i in range(len(sks)):
                if i % colNum == cn:
                    col.append({'k':sks[i],'v':sorted(cate[k][sks[i]])})
            cols.append(col)
        nav['cols'] = cols
        navs.append(nav)
    return navs
def getItemPrice(it):
  if it.sales_price > 0:
    return it.sales_price
  return it.price

def toStructuredItem(it):
  res =  {'name' : it.name, 'price' : it.price, 'category' : it.category,
      'id' : it.id, 'tax_class' : it.tax_class, 'sku' : it.sku, 'store': it.store.name,
      'remark': it.remark}
  if it.sales_price > 0:
    res['sales_price'] = it.sales_price
  return res

def extractCate(query):
  patterns = ['cate:"([^"]*)"', 'cate:([^ "]*)',]
  cate = []
  r = query
  for p in patterns:
    cate.extend(re.findall(p, r))
    r = re.sub(p, '', r)
  return cate, r

def extractStore(query):
  patterns = ["store:([^ ]*)",]
  store = []
  r = query
  for p in patterns:
    store.extend(re.findall(p, r))
    r = re.sub(p, '', r)
  return store, r

def getRawItemsByQuery(query):
  cates,query = extractCate(query)
  stores,query = extractStore(query)
  if cates:
    cate = cates[0]
  else:
    cate = ''
  if stores:
    store = stores[0]
  else:
    store = ''
  keyword = re.sub(r'^\s*|\s*$', '', query)
  res = Item.objects.all().filter(store__name__icontains=store).filter(category__icontains=cate)
  for k in keyword.split():
    res = res.filter(Q(name__icontains=k+' ') | Q(name__icontains=' '+k) | Q(remark__icontains='"%s"' % k))
  return res.exclude(out_of_stock=1)

def getItemsByRange(query, startId, num):
  return map(toStructuredItem, getRawItemsByQuery(query)[startId : startId + num])

def getPopularItemsByRange(query, startId, num):
  return map(toStructuredItem, getRawItemsByQuery(query).order_by('-sold_number')[startId : startId + num])

def getItemsByIds(ids):
  return map(toStructuredItem, Item.objects.filter(id__in = set(ids)))

def computeTax(item):
  if item['tax_class'] == 'zero-rate':
    return 0
  elif item['tax_class'] == 'standard-rate':
    return TAX_RATE * item['price']
  else:
    return 0

def computeDelivery(item):
  return 4.0

import urllib2

def getItemsInternal(request, getItemCallback):
  if request.method == 'POST':
    if 'startId' in request.POST:
      query = request.POST['query']
      query = urllib2.unquote(query.encode("utf8"))
      startId = int(request.POST['startId'])
      num = int(request.POST['num'])
      return HttpResponse(json.dumps(getItemCallback(query, startId, num)))
    elif 'ids' in request.POST:
      ids = json.loads(request.POST['ids'])
      return HttpResponse(json.dumps(getItemsByIds(ids)))
    else:
      return HttpResponse('error')
  else:
    return HttpResponse('error')

@csrf_exempt
def getItems(request):
  return getItemsInternal(request, getItemsByRange)

@csrf_exempt
def getPopularItems(request):
  return getItemsInternal(request, getPopularItemsByRange)

def computeSummaryInternal(idsStr):
    ids = json.loads(idsStr)
    items = getItemsByIds(ids)
    d = computeDelivery(items)
    s = 0.0
    t = 0.0
    for item in items:
      ct = ids.count(item['id'])
      if 'sales_price' in item:
        s += item['sales_price'] * ct
      else:
        s += item['price'] * ct
      t += computeTax(item) * ct
    return {'sum' : s, 'tax' : t, 'delivery' : d, 'total' : s + t + d}

@csrf_exempt
def computeSummary(request):
  if request.method == 'POST':
    res = computeSummaryInternal(request.POST['ids'])
    return HttpResponse(json.dumps(res))
  else:
    return HttpResponse('error')
