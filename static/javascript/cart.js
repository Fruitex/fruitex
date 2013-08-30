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
        .append($('<td>').attr('class', 'summary-label').text('Tax : '))
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
}

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

var isValidUserInput = function () {
  var v = InputValidator;
  v.init();
  return v.nonEmpty($("input[name=name]")) && v.nonEmpty($("input[name=phone]"))
      && v.nonEmpty($("input[name=address]")) && v.nonEmpty($("input[name=postcode]"))
      && v.phone($("input[name=phone]")) && v.zip($("input[name=postcode]"));
}

$(document).ready(function() {
  if (!isCartEmpty()) {
    var list = loadItemsInCart();
    $('body').on('change', '.num-spinner', 
      function (evt) {
        writeToCookie();
        list.updatePrice(this.id);
        showSummary();
      });
    $('body').on('spinstop', '.num-spinner', 
      function (evt) {
        writeToCookie();
        list.updatePrice(this);
        showSummary();
      });
  } else {
    $('#items-in-cart-summary-container').remove();
    $('#cart-footer').remove();
    $('#delivery-wrapper').remove();
    $("#cart-container").append($('<p>').text('Seems like your cart is empty.').addClass('cart-empty-msg'));
  }
});
