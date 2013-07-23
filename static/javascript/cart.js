var loadItemsInCart= function() {
  var itemIds = $.cookie('cart');
  var itemCountGetter = function(id) {
    var res = 0;
    for (var i = 0; i < itemIds.length; i++) {
      if (itemIds[i] == id) {
        res++;
      }
    }
    return res;
  };
  $.post('/items/getItems',
    {'ids' : itemIds}, 
    function(data) {
      if (data.length > 0) {
        showItemsInCart(data, itemCountGetter);
      }
      $('.num-spinner').spinner({
        min: 0,
        max: 100,
        step: 1,
      });
    }, 'json');
};
var showSummary = function() {
  var table = $('#items-in-cart-summary-table');
  if (table.length == 0) {
    var itemsSummary = $('#items-in-cart-summary-container');
    table = $('<table>').attr('id', 'items-in-cart-summary-table');
    itemsSummary.append(table);
  }
  $.post('/items/computeSummary',
    {'ids' : $.cookie('cart')},
    function(data) {
      table.append($('<tr>').attr('id', 'summary-sum')
        .append($('<td>').attr('class', 'summary-label').text('Sum : '))
        .append($('<td>').attr('class', 'summary-value').text('$ ' + data.sum.toFixed(2))))
      .append($('<tr>').attr('id', 'summary-tax')
        .append($('<td>').attr('class', 'summary-label').text('Tax : '))
        .append($('<td>').attr('class', 'summary-value').text('$ ' + data.tax.toFixed(2))))
      .append($('<tr>').attr('id', 'summary-delivery')
        .append($('<td>').attr('class', 'summary-label').text('Delivery : '))
        .append($('<td>').attr('class', 'summary-value').text('$ ' + data.delivery.toFixed(2))))
      .append($('<tr>').attr('id', 'summary-total')
        .append($('<td>').attr('class', 'summary-label').text('Total : '))
        .append($('<td>').attr('class', 'summary-value').text('$ ' + data.total.toFixed(2))));

      $('#checkout-button').click(function() {
        var name = $('#delivery_name')[0].value;
        var phone = $('#delivery_phone')[0].value;
        var address = $('#delivery_address')[0].value;
        var postcode = $('#delivery_postcode')[0].value;
        var itemIds = $.cookie('cart');
        $.post('/cart/checkout',
        {
          'name' : name,
          'phone' : phone,
          'address' : address,
          'postcode' : postcode,
          'ids' : itemIds,
          'price' : data.sum,
          'tax' : data.tax,
          'shipping' : data.delivery
        }, 
        function(data) {
          alert(data);
        }, 'json');
      });
    }, 
    'json');
};

var showItemsInCart = function(items, itemCountGetter) {
  var container = $('#cart-container');
  for (var i = 0; i < items.length; i++) {
    container.append(createItemInCart(items[i], itemCountGetter(items[i].id)));
  }
  showSummary();
};

var createItemInCart = function(item, count) {
  return $('<div>').attr('class', 'item-in-cart')
  .append($('<div>').attr('class', 'item-in-cart-img'))
  .append($('<div>').attr('class', 'item-info-wrapper')
    .append($('<span>').attr('class', 'item-in-cart-name').text(item.name))
    .append($('<input>').attr('class', 'num-spinner').attr('value', count).attr('id', item.id))
    .append($('<span>').attr('class', 'item-in-cart-price').text('$ ' + item.price)));
};

var writeToCookie = function() {
  var ItemsIds = [];
  for (var j = 0; j < $(".ui-spinner-input").length; j++) {
    var spinner = $(".ui-spinner-input")[j];
    for (var i = 0; i < spinner.value; i++) {
      ItemsIds.push(parseInt(spinner.id));
    }
  }
  $.cookie('cart', JSON.stringify(ItemsIds), { path: '/' });
}

$(document).ready(function() {
  loadItemsInCart();
  $('body').on('change', '.num-spinner', 
    function (evt) {
      writeToCookie();
  });
  $('body').on('spinstop', '.num-spinner', 
    function (evt) {
      writeToCookie();
  });
});
