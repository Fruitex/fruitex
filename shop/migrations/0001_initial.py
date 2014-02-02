# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Store'
        db.create_table(u'shop_store', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('display_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'shop', ['Store'])

        # Adding model 'StoreCustomization'
        db.create_table(u'shop_storecustomization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.OneToOneField')(related_name='customization', unique=True, to=orm['shop.Store'])),
            ('featured', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('show_banner', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('show_on_sale', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('show_best_selling', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'shop', ['StoreCustomization'])

        # Adding model 'DeliveryOption'
        db.create_table(u'shop_deliveryoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(related_name='delivery_options', to=orm['shop.Store'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('display_format', self.gf('django.db.models.fields.CharField')(default='{start_date} {start_time} ~ {end_time}', max_length=256)),
            ('start_time', self.gf('django.db.models.fields.IntegerField')()),
            ('time_interval', self.gf('django.db.models.fields.IntegerField')()),
            ('monday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tuesday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('wednesday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('thursday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('friday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('saturday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sunday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2)),
        ))
        db.send_create_signal(u'shop', ['DeliveryOption'])

        # Adding model 'Category'
        db.create_table(u'shop_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(related_name='categories', on_delete=models.PROTECT, to=orm['shop.Store'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sub_categories', null=True, to=orm['shop.Category'])),
        ))
        db.send_create_signal(u'shop', ['Category'])

        # Adding model 'Item'
        db.create_table(u'shop_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', on_delete=models.PROTECT, to=orm['shop.Category'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sku', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2)),
            ('sales_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=16, decimal_places=2)),
            ('tax_class', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=3, decimal_places=2)),
            ('out_of_stock', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('on_sale', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('max_quantity_per_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('featured', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('sold_number', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('when_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('when_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'shop', ['Item'])

        # Adding model 'ItemMetaFilter'
        db.create_table(u'shop_itemmetafilter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('filterable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'shop', ['ItemMetaFilter'])

        # Adding model 'ItemMeta'
        db.create_table(u'shop_itemmeta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='metas', to=orm['shop.Item'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'shop', ['ItemMeta'])


    def backwards(self, orm):
        # Deleting model 'Store'
        db.delete_table(u'shop_store')

        # Deleting model 'StoreCustomization'
        db.delete_table(u'shop_storecustomization')

        # Deleting model 'DeliveryOption'
        db.delete_table(u'shop_deliveryoption')

        # Deleting model 'Category'
        db.delete_table(u'shop_category')

        # Deleting model 'Item'
        db.delete_table(u'shop_item')

        # Deleting model 'ItemMetaFilter'
        db.delete_table(u'shop_itemmetafilter')

        # Deleting model 'ItemMeta'
        db.delete_table(u'shop_itemmeta')


    models = {
        u'shop.category': {
            'Meta': {'object_name': 'Category'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sub_categories'", 'null': 'True', 'to': u"orm['shop.Category']"}),
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