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
    if not Store.objects.filter(name=store_name).exists():
      store = Store(name = store_name, slug = store_name, address = 'TBD')
      store.save()
    for row in spamreader:
      if rownum == 0:
        # Store header row and recognize column name accordingly
        head = row
        rownum = 1
        for index, item in enumerate(head):
          if item == "Name":
              name_index = index
          elif item == "Category":
              category_index = index
          elif item == "Description":
              description_index = index
          elif item == "SKU":
              sku_index = index
          elif item == "Price":
              price_index = index
          elif item == "Tax Class":
              tax_class_index = index
          else:
              # metaList (key=index, value = column_title)
              metaList[index] = item
      else:
        p1 = Item()
        for index, item in enumerate(row):
          # Add Item attributes according to column index
          if index == name_index:
            p1.name = row[name_index]
          elif index == category_index:
            catParent = ''
            result = re.split('->', row[category_index])
            # Split up Category content, interate from top layer
            for catName in result:
              if not Category.objects.filter(name=catName).exists():
                # If no such Category exists
                if not catParent=='':
                  # Category don't have a parent
                  p = Category.objects.create(name = catName, store = Store.objects.get(name = store_name),
                      parent = Category.objects.get(name = catParent))
                else:
                  p = Category.objects.create(name = catName, store = Store.objects.get(name = store_name))
              # Remember current category(parent for next level)
              catParent = catName
            # Assign item's category and we know it exists now
            p1.category = Category.objects.get(name = catName)
          elif index == description_index:
            p1.description = row[description_index]
          elif index == sku_index:
            p1.sku = row[sku_index]
          elif index == price_index:
            p1.price = Decimal(row[price_index])
          elif index == tax_class_index:
            p1.tax_class = Decimal(row[tax_class_index])
          else:
            # Any other column index belong to metaData
            m = ItemMeta()
            # Retrieve column name from metaList
            m.key = metaList[index]
            m.value = item
            # We can't save itemMeta until the Item is saved
            itemMeta.append(m)
        p1.save()
        for me in itemMeta:
          # Now Item is successfully saved, we can save all lingering meta
          me.item = p1
          me.save()
        # Flush metaData list for next row
        del itemMeta[:]

