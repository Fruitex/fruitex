var showItems = function (items) {
  var itemList = $('#item-list').empty();
  for (var i = 0; i < items.length; i++) {
    var item = items[i];
    var itemContainer = $('<div>').attr('class', 'item-container');
    itemList.append(itemContainer);
    var itemInfo = $('<div>').attr('class', 'item-info-wrapper')
    .append($('<div>').attr('class', 'item-image'))
    .append($('<div>').attr('class', 'item-name').text(item.name))
    .append($('<div>').attr('class', 'item-price').text(item.price))
    .append($('<div>').attr('class', 'item-category').text(item.category));
    var btn = $('<div>').attr('class', 'btn-add-container')
    .append($('<img>')
      .attr('class', 'btn-add')
      .attr('src', '/static/imgs/btn_add.png'));
    btn.click((function(id) {
      return function() { addToCart(id); }
    })(item.id));
    itemContainer.hover(
      function () {
        $(this).children('.btn-add-container').slideDown('fast');
      }, function () {
        $(this).children('.btn-add-container').slideUp('fast');
      });  
    itemContainer.append(itemInfo).append(btn);
  }
};
var addToCart = function(itemId) {
  var cart;
  if ($.cookie("cart") == undefined) {
    cart = new Array();
  } else {
    cart = JSON.parse($.cookie("cart"));
  }
  cart.push(itemId);
  $.cookie("cart", JSON.stringify(cart), {path : '/'});
  addToCartAnimation();
  updateCartBubble();
};

var addToCartAnimation = function() {
	$("#img_add_success").fadeIn(500, function () {
		setTimeout(function () {$("#img_add_success").fadeOut(1000);}, 2000);
	});
}

var updateCartBubble = function() {
	$("#cart_bubble").hide();
	var size = $.cookie("cart") == undefined ? 0 : JSON.parse($.cookie("cart")).length;
	if (size > 0) {
		$("#cart_bubble").show();
		$("#cart_bubble").children("p").text(size);
	}
}

var getAndShowItems = function(query, startId, num) {
  $.post('/items/getItems',
    {'startId' : startId, 'num' : num, 'query' : query}, 
    function(data) {
      if (data.length > 0) {
        showItems(data);
        $('#navigator-prev').unbind('click').click(function() {
          if (startId > 0) {
            getAndShowItems(query, startId - num, num);
          }
        });
        $('#navigator-next').unbind('click').click(function() {
          getAndShowItems(query, startId + num, num)
        });
      }
    }, 'json');
};

$(document).ready(function () {
  updateCartBubble();
  var query = getURLParameter('query');
  getAndShowItems(query, 0, 12);
  $(".item-container").hover(function() {
    $(this).children(".btn-add-container").slideDown('fast');
  }, function () {
    $(this).children(".btn-add-container").slideUp('fast');
  });
});