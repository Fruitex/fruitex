#!/usr/bin/env python
import csv
import re
from decimal import Decimal
from shop.models import Store, Category, Item, ItemMeta

def import_from_csv(filename, store_name):
  print 'Starting to import from CSV file %s' % filename
  with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
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
    
    # Store
    if not Store.objects.filter(name=store_name).exists():
      store = Store.objects.create(name = store_name, 
        slug = (store_name.lower()).replace(" ", "_"), address = 'TBD')
    for row in csvreader:
      if rownum == 0:
        # Store header row and recognize column name accordingly
        head = row
        rownum = 1
        for index, colname in enumerate(head):
          if colname == "Name":
              name_index = index
          elif colname == "Category":
              category_index = index
          elif colname == "Description":
              description_index = index
          elif colname == "SKU":
              sku_index = index
          elif colname == "Price":
              price_index = index
          elif colname == "Tax Class":
              tax_class_index = index
          else:
              # metaList (key=index, value = column_title)
              metaList[index] = colname
      else:
        item = Item()
        itemMeta = []
        for value, attribute in enumerate(row):
          # Add Item attributes according to column index
          if value == name_index:
            item.name = row[name_index]
          elif value == category_index:
            catParent = ''
            result = re.split('->', row[category_index])
            # Split up Category content, iterate from top layer
            for catName in result:
              if not Category.objects.filter(name=catName).exists():
                # If no such Category exists
                slugName = (catName.lower()).replace(" ", "_")
                if not catParent=='':
                  # Current category has a parent
                  p = Category.objects.create(name = catName, slug = slugName, 
                      store = Store.objects.get(name = store_name),
                      parent = Category.objects.get(name = catParent))
                else:
                  # Current category is of top layer(eg.Beverages)
                  p = Category.objects.create(name = catName, slug = slugName, 
                      store = Store.objects.get(name = store_name))
              # Remember current category(as parent for next layer cat)
              catParent = catName
            # Assign Item's category since we know it exists now
            item.category = Category.objects.get(name = catName)
          elif value == description_index:
            item.description = row[description_index]
          elif value == sku_index:
            item.sku = row[sku_index]
          elif value == price_index:
            item.price = Decimal(row[price_index])
          elif value == tax_class_index:
            item.tax_class = Decimal(row[tax_class_index])
          else:
            # Any other column index belong to metaData
            m = ItemMeta()
            # Retrieve column name from metaList
            m.key = metaList[value]
            m.value = attribute
            # We can't save itemMeta until the Item is saved
            itemMeta.append(m)
        item.save()
        for me in itemMeta:
          # Now Item is successfully saved, we can save all lingering meta
          me.item = item
          me.save()
