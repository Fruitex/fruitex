#!/usr/bin/env python
import os
import sys
import json
import re

def clearItems():
  for o in Store.objects.all():
    o.delete()
  for o in Item.objects.all():
    o.delete()

def _getAllCsvFiles(folder):
  res = []
  for f in os.listdir(folder):
    if f.endswith('.csv'):
      res.append(folder + f)
    elif os.path.isdir(folder + f):
      res.extend(_getAllCsvFiles(folder + f + os.path.sep))
  return res

def showOrders():
  for o in Order.objects.all():
    print o

def trim(s):
  return re.sub('(^\s+|\s+$)', '', s)

def loadItems():
  import csv
  sobeys = Store(name = 'sobeys',
      address = "450 Columbia St W, Waterloo ON N2T 2W1")
  sobeys.save()
  items = []

  for fname in _getAllCsvFiles('data/'):
    f = csv.reader(open(fname))
    next(f) # eat the header 
    print fname
    for lst in f:
      items.append((map(trim, lst), fname))
  TITLE=0
  CATEGORY=3
  PRICE=5
  SALES_PRICE=7
  WEIGHT=8
  LENGTH=9
  WIDTH=10
  HEIGHT=11
  SKU=12
  TAX_STATUS=15
  TAX_CLASS=16

  def getRemark(item):
    res = {}
    if item[WEIGHT]:
      res["weight"] = item[WEIGHT]
    if item[LENGTH]:
      res["length"] = item[LENGTH]
    if item[WIDTH]:
      res["width"] = item[WIDTH]
    if item[HEIGHT]:
      res["height"] = item[HEIGHT]
    if item[SALES_PRICE]:
      res["sales_price"] = item[SALES_PRICE]
    return json.dumps(res)

  print "%d items to write" % len(items)
  ct = 0
  problemFiles = set()
  for item,fname in items:
    try:
      if item[CATEGORY] and item[TITLE] and item[SKU] and item[PRICE] \
          and item[TAX_STATUS] and item[TAX_CLASS]:
        Item(store = sobeys, category = item[CATEGORY],
            name = item[TITLE], price = item[PRICE], sku = item[SKU],
            tax_status = item[TAX_STATUS], tax_class = item[TAX_CLASS],
            remark = getRemark(item)).save()
      else:
        if fname in problemFiles:
          continue
        else:
          problemFiles.add(fname)
          print 'data in %s is not complete' % fname
          print item
    except Exception as e:
      print e, fname, item
    ct += 1
    if ct%100==0:
      print "%d items written" % ct

def fetchCategory():
  res = set()
  for it in Item.objects.all():
    res.add(it.category)
  for c in res:
    print c

def showTax():
  tax={}
  for o in Item.objects.all():
    s = o.tax_class
    if s in tax:
      tax[s]+=1
    else:
      tax[s] = 1
  print tax

def main(argv):
  if len(argv) > 1 and argv[1] == 'clear':
    clearItems()
  elif len(argv) > 1 and argv[1] == 'load':
    loadItems()
  elif len(argv) > 1 and argv[1] == 'cate':
    fetchCategory()
  elif len(argv) > 1 and argv[1] == 'order':
    showOrders()
  elif len(argv) > 1 and argv[1] == 'tax':
    showTax()
  else:
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fruitex.settings")
  from home.models import Store, Item
  from cart.models import Order
  main(sys.argv)

