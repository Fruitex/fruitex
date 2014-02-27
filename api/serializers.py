from rest_framework import serializers

from shop.models import Store, Item
from order.models import DeliveryWindow, Invoice, Order, OrderItem


class StoreSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Store
    fields = ('id', 'url', 'name', 'address')

class ItemSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Item
    fields = ('id', 'url', 'name', 'description',
              'price', 'sales_price', 'on_sale', 'out_of_stock', 'featured',
              'max_quantity_per_order', 'sold_number', 'when_added', 'when_updated')


class DeliveryWindowSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = DeliveryWindow
    fields = ('id', 'url', 'start', 'end')

class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Invoice
    fields = ('id', 'url', 'invoice_num',
              'status', 'payer', 'when_created', 'when_updated',
              'subtotal', 'tax', 'delivery', 'discount',
              'customer_name', 'address', 'postcode', 'phone', 'email')

class OrderSerializer(serializers.HyperlinkedModelSerializer):
  items = serializers.HyperlinkedRelatedField(view_name='orderitem-detail', many=True)

  class Meta:
    model = Order
    fields = ('id', 'url', 'items',
              'subtotal', 'tax', 'delivery_window', 'comment',
              'invoice', 'status', 'when_created', 'when_updated')

class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = OrderItem
    fields = ('id', 'url', 'item', 'order', 'allow_sub', 'quantity', 'item_cost', 'item_tax')
