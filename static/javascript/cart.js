var showSummary = function() {
  $('#items-in-cart-summary-table').remove();
  var itemsSummary = $('#items-in-cart-summary-container');
  var table = $('<table>').attr('id', 'items-in-cart-summary-table');
  itemsSummary.append(table);
  $.post('/home/computeSummary',
    {'ids' : $.cookie('cart')},
    function(data) {
      table.append($('<tr>').attr('id', 'summary-sum')
        .append($('<td>').attr('class', 'summary-label').text('Sum : '))
        .append($('<td>').attr('class', 'summary-value').text('$ ' + data.sum.toFixed(2))))
      .append($('<tr>').attr('id', 'summary-tax')
        .append($('<td>').attr('class', 'summary-label').text('HST : '))
        .append($('<td>').attr('class', 'summary-value').text('$ ' + data.tax.toFixed(2))))
      .append($('<tr>').attr('id', 'summary-delivery')
        .append($('<td>').attr('class', 'summary-label').text('Delivery : '))
        .append($('<td>').attr('class', 'summary-value').text('$ ' + data.delivery.toFixed(2))))
      .append($('<tr>').attr('id', 'summary-total')
        .append($('<td>').attr('class', 'summary-label').text('Total : '))
        .append($('<td>').attr('class', 'summary-value').text('$ ' + data.total.toFixed(2))));
    }, 
    'json');
};

var updatePrice = function(spinner) {
  $(spinner).parent().children('.item-in-cart-price')
}

var loadItemsInCart = function() {
  var itemIds = JSON.parse($.cookie('cart'));
  var list = ItemList(itemIds, true);
  list.generate($("#cart-container"), showSummary);
  return list;
};

var isCartEmpty = function() {
  return !$.cookie('cart') || JSON.parse($.cookie('cart')).length == 0;
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
};

var disableDeliveryTime = function(btn) {
  btn.attr('disabled', true);
  btn.parent().addClass('disabled')
}
var checkDeliveryTime = function() {
  var d = new Date();
  var h = d.getHours();
  if (h > 11) {
    disableDeliveryTime($('input[value="12:00-14:00"]'));
  }
  if (h > 15) {
    disableDeliveryTime($('input[value="16:00-18:00"]'));
  }
  if (h > 19) {
    disableDeliveryTime($('input[value="20:00-22:00"]'));
  }
}

var clearCart = function() {
  $.cookie('cart', '', { path: '/' });
};

var isValidUserInput = function() {
  var v = InputValidator;
  v.init();
  return v.nonEmpty($("input[name=name]")) && v.nonEmpty($("input[name=phone]"))
      && v.nonEmpty($("input[name=address]")) && v.nonEmpty($("input[name=postcode]"))
      && v.phone($("input[name=phone]")) && v.zip($("input[name=postcode]"));
};

$(document).ready(function() {
  checkDeliveryTime();
  if (!isCartEmpty()) {
    var list = loadItemsInCart();
    $('body').on('change', '.num-spinner', 
      function (evt) {
        writeToCookie();
        list.updatePrice(this.id);
        $("#delivery_item_ids").attr('value', $.cookie('cart'));
        showSummary();
      });
    $('body').on('spinstop', '.num-spinner', 
      function (evt) {
        writeToCookie();
        list.updatePrice(this);
        $("#delivery_item_ids").attr('value', $.cookie('cart'));
        showSummary();
      });
  } else {
    $('#items-in-cart-summary-container').remove();
    $('#cart-footer').remove();
    $('#delivery-wrapper').remove();
    $("#cart-container").append($('<p>').text('Seems like your cart is empty.').addClass('cart-empty-msg'));
    $("#cart-container").append($('<p>').text('Return to shop')
      .addClass('cart-btn-return')
      .click(function () {
        window.location = '/home/';
      }));
  }
});
