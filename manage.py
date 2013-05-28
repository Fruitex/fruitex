#!/usr/bin/env python
import os
import sys

def clearItems():
  from items.models import Store, Item
  for o in Store.objects.all():
    o.delete()
  for o in Item.objects.all():
    o.delete()

def loadItems():
  from items.models import Store, Item
  import csv
  sobeys = Store(name = 'sobeys',
      address = "450 Columbia St W, Waterloo ON N2T 2W1")
  sobeys.save()
  items = []

  for fname in os.listdir("items/data"):
    f = csv.reader(open("items/data/%s" % fname))
    next(f) # eat the header 
    for lst in f:
      items.append(lst)
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
    res = ""
    if item[WEIGHT]:
      res += "weight: %s; " % item[WEIGHT]
    if item[LENGTH]:
      res += "length: %s;" % item[LENGTH]
    if item[WIDTH]:
      res += "width: %s;" % item[WIDTH]
    if item[HEIGHT]:
      res += "height: %s;" % item[HEIGHT]
    if item[SALES_PRICE]:
      res += "sales_price: %s;" % item[SALES_PRICE]
    return res

  for item in items:
    Item(store = sobeys, category = item[CATEGORY],
        name = item[TITLE], price = item[PRICE], sku = item[SKU],
        tax_status = item[TAX_STATUS], tax_class = item[TAX_CLASS],
        remark = getRemark(item)).save()

def main(argv):
  if len(argv) > 1 and argv[1] == 'clear':
    clearItems()
  elif len(argv) > 1 and argv[1] == 'load':
    loadItems()
  else:
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fruitex.settings")
  main(sys.argv)

