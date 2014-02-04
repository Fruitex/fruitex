# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Category.shop_order'
        db.add_column(u'shop_category', 'shop_order',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Category.shop_location_note'
        db.add_column(u'shop_category', 'shop_location_note',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Category.shop_order'
        db.delete_column(u'shop_category', 'shop_order')

        # Deleting field 'Category.shop_location_note'
        db.delete_column(u'shop_category', 'shop_location_note')


    models = {
        u'shop.category': {
            'Meta': {'object_name': 'Category'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sub_categories'", 'null': 'True', 'to': u"orm['shop.Category']"}),
            'shop_location_note': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'shop_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'categories'", 'on_delete': 'models.PROTECT', 'to': u"orm['shop.Store']"})
        },
        u'shop.deliveryoption': {
            'Meta': {'object_name': 'DeliveryOption'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'display_format': ('django.db.models.fields.CharField', [], {'default': "'{start_date} {start_time} ~ {end_time}'", 'max_length': '256'}),
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'start_time': ('django.db.models.fields.IntegerField', [], {}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'delivery_options'", 'to': u"orm['shop.Store']"}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'time_interval': ('django.db.models.fields.IntegerField', [], {}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'shop.item': {
            'Meta': {'object_name': 'Item'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'on_delete': 'models.PROTECT', 'to': u"orm['shop.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'featured': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_quantity_per_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'on_sale': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'out_of_stock': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'sales_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '16', 'decimal_places': '2'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sold_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tax_class': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '3', 'decimal_places': '2'}),
            'when_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'when_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'shop.itemmeta': {
            'Meta': {'object_name': 'ItemMeta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'metas'", 'to': u"orm['shop.Item']"}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'shop.itemmetafilter': {
            'Meta': {'object_name': 'ItemMetaFilter'},
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'filterable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'shop.store': {
            'Meta': {'object_name': 'Store'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'shop.storecustomization': {
            'Meta': {'object_name': 'StoreCustomization'},
            'featured': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'show_banner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_best_selling': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_on_sale': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'store': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'customization'", 'unique': 'True', 'to': u"orm['shop.Store']"})
        }
    }

    complete_apps = ['shop']