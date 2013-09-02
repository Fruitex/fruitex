#!/usr/bin/env python
import os
import sys
import json
import csv
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


def loadBooks():
  bookstore = Store(name = 'bookstore', address = "")
  bookstore.save()
  items = []
  for fname in _getAllCsvFiles('data/bookstore/'):
    f = csv.reader(open(fname))
    next(f) # eat the header 
    print fname
    for lst in f:
      items.append((map(trim, lst), fname))
  DPT=0
  CRS=1
  SECTION=2
  E_EN=3
  PROV=4
  RO=5
  AUTHOR=6
  TITLE=7
  VL=8
  ED=9
  PUBLISHER=10
  CP=11
  B=12
  PRICE=13
  CATEGORY=14
  PIC=15
  TAX_STATUS=16
  TAX_CLASS=17

  def getRemark(item):
    res = {}
    if item[DPT]:
      res["dpt"] = item[DPT]
    if item[CRS]:
      res["crs"] = item[CRS]
    if item[SECTION]:
      res["section"] = item[SECTION]
    if item[E_EN]:
      res["e/en"] = item[E_EN]
    if item[PROV]:
      res["prov"] = item[PROV]
    if item[RO]:
      res["r/o"] = item[RO]
    if item[AUTHOR]:
      res["author"] = item[AUTHOR]
    if item[VL]:
      res["vl"] = item[VL]
    if item[ED]:
      res["ed"] = item[ED]
    if item[PUBLISHER]:
      res["publisher"] = item[PUBLISHER]
    if item[CP]:
      res["cp"] = item[CP]
    if item[B]:
      res["b"] = item[B]
    if item[PIC]:
      res["pic"] = item[PIC]
    return json.dumps(res)

  print "%d books to write" % len(items)
  ct = 0
  problemFiles = set()
  for item,fname in items:
    try:
      if item[CATEGORY] and item[TITLE] and item[PRICE] \
          and item[TAX_STATUS] and item[TAX_CLASS]:
        Item(store = bookstore, category = item[CATEGORY],
            name = item[TITLE], price = item[PRICE], sku = os.path.splitext(item[PIC])[0],
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
      print "%d books written" % ct

def loadItems():
  sobeys = Store(name = 'sobeys', address = "450 Columbia St W, Waterloo ON N2T 2W1")
  sobeys.save()
  items = []
  for fname in _getAllCsvFiles('data/sobeys/'):
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

def fixTypo():
  ct = 0
  for o in Item.objects.all():
    if 'Goceries' in  o.category:
      o.category = o.category.replace('Goceries', 'Groceries')
      o.save()
      ct += 1
  print '%d items fixed' % ct

def main(argv):
  if len(argv) > 1 and argv[1] == 'clear':
    clearItems()
  elif len(argv) > 1 and argv[1] == 'load':
    loadItems()
    loadBooks()
  elif len(argv) > 1 and argv[1] == 'cate':
    fetchCategory()
  elif len(argv) > 1 and argv[1] == 'order':
    showOrders()
  elif len(argv) > 1 and argv[1] == 'tax':
    showTax()
  elif len(argv) > 1 and argv[1] == 'fix':
    fixTypo()
  else:
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fruitex.settings")
  from home.models import Store, Item
  from cart.models import Order
  main(sys.argv)

