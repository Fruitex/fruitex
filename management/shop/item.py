#!/usr/bin/env python
import csv
import re
from decimal import Decimal
from shop.models import Store, Category, Item, ItemMeta

def import_from_csv(filename, store_name):
  print 'Starting to import from CSV file %s' % filename
  with open(filename, 'rU') as csvfile:
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
    StoreQS = Store.objects.filter(name=store_name)
    store = None
    if not StoreQS.exists():
      store = Store.objects.create(
        name = unicode(store_name),
        slug = (store_name.lower()).replace(" ", "_"),
        address = 'TBD'
      )
    else:
      store = StoreQS[0]

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
        try:
          item = Item()
          itemMeta = []
          for value, attribute in enumerate(row):
            # Add Item attributes according to column index
            if value == name_index:
              item.name = unicode(row[name_index])
            elif value == category_index:
              category = None
              names = re.split('->', row[category_index])
              allCategories = Category.objects.filter(store=store)

              # Split up Category content, iterate from top layer
              for name in names:
                categories = allCategories.filter(name=name)
                if category is None:
                  # If is top layer, try to find a category without parent
                  categories = categories.filter(parent__isnull=True)
                else:
                  categories = categories.filter(parent=category)

                if not categories.exists():
                  # If no such Category exists, create one
                  slug = name.lower().replace(" ", "_")
                  category = Category.objects.create(
                    name = name,
                    slug = slug,
                    store = store,
                    parent = category,
                  )
                else:
                  category = categories[0]

              # Assign Item's category since we know it exists now
              item.category = category
            elif value == description_index:
              item.description = unicode(row[description_index].decode('utf-8'))
            elif value == sku_index:
              item.sku = unicode(row[sku_index])
            elif value == price_index:
              item.price = Decimal(row[price_index])
            elif value == tax_class_index:
              item.tax_class = Decimal(row[tax_class_index])
            else:
              # Any other column index belong to metaData
              meta = ItemMeta()
              # Retrieve column name from metaList
              meta.key = unicode(metaList[value])
              meta.value = unicode(attribute)
              # We can't save itemMeta until the Item is saved
              itemMeta.append(meta)
          item.save()
        except Exception as e:
          print row[name_index]
          print e
        for meta in itemMeta:
          # Now Item is successfully saved, we can save all lingering meta
          meta.item = item
          meta.save()
