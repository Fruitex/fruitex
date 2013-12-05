#!/usr/bin/env python
import os
import sys
import csv
import re
from decimal import Decimal
from shop.models import Store, Category, Item, ItemMeta


def import_from_csv(filename, store_name):
  print 'Starting to import from CSV file %s' % filename
  with open(filename, 'r') as csvfile:

    print 'file opened'

    spamreader = csv.reader(csvfile)
    
    rownum = 0

    # Remember Col index

    name_index = -1
    category_index = -1
    description_index = -1
    sku_index = -1
    price_index = -1
    tax_class_index = -1

    # ItemMeta list
    metaList = dict()
    itemMeta = []

    # Store
    if (not(Store.objects.filter(name=store_name).exists())):
      store = Store(name = store_name)
      store.slug = store_name
      store.address = 'TBD'
      store.save()

    for row in spamreader:
      if rownum == 0:
        head = row
        rownum = 1
        for index, item in enumerate(head):
          if (item == "Name"):
              name_index = index
              print 'name = '+str(name_index)
          elif (item == "Category"):
              category_index = index
              print 'category = '+str(category_index)
          elif (item == "Description"):
              description_index = index
              print 'description = '+str(description_index)
          elif (item == "SKU"):
              sku_index = index
              print 'sku = '+str(sku_index)
          elif (item == "Price"):
              price_index = index
              print 'price = '+str(price_index)
          elif (item == "Tax Class"):
              tax_class_index = index
              print 'tax_class = '+str(tax_class_index) 
          else:
              metaList[index] = item
              print metaList


      else:
        p1 = Item()
        for index, item in enumerate(row):
          

          if (index == name_index):
            p1.name = row[name_index]
          elif (index == category_index):

            catParent = ''

            result = re.split('->', row[category_index])

            for catName in result:
              if (not(Category.objects.filter(name=catName).exists())):
                if (not(catParent=='')):
                  p = Category.objects.create(name = catName, store = Store.objects.get(name = store_name),
                      parent = Category.objects.get(name = catParent))
                else:
                  p = Category.objects.create(name = catName, store = Store.objects.get(name = store_name))
              catParent = catName
            p1.category = Category.objects.get(name = catName)
          elif (index == description_index):
            p1.description = row[description_index]
          elif (index == sku_index):
            p1.sku = row[sku_index]
          elif (index == price_index):
            p1.price = Decimal(row[price_index])
          elif (index == tax_class_index):
            p1.tax_class = Decimal(row[tax_class_index])
          
          else:
            m = ItemMeta()
            m.key = metaList[index]
            m.value = item
            itemMeta.append(m)
        p1.save()
        for me in itemMeta:
          me.item = p1
          me.save()
        del itemMeta[:]
    

  print Store.objects.all()
  print Category.objects.all()
  print Item.objects.all()
  print ItemMeta.objects.all()

