{% load static %}

var isSearchResult = function() {
  var query = ParseQuery(getURLParameter('query'));
  return query.cate.length || query.keyword.length;
}

var isBook = function(item) {
  return item.remark &&
         JSON.parse(item.remark) &&
         JSON.parse(item.remark)["crs"];
};

var createPrice = function (price) {
  return $('<div>').addClass('item-price')
      .append($('<span>').text('$' + price))
      .append($('<img>').attr('src', '{% static "imgs/tag_cad.png" %}'));
}

var generateItems = function (items, container, isPopular) {
  var itemList = container.empty();
  if (isPopular) {
    itemList.append($('<p>').text('What\'s popular in ' + GetSelectedStoreDisplay()).addClass('popular-item-list-title'));
  }
  for (var i = 0; i < items.length; i++) {
    var item = items[i];
    var containerClassName = 'item-container';
    if (isPopular) {
      containerClassName = 'popular-item-container';
    }
    var itemContainer = $('<div>').attr('class', containerClassName);
    itemList.append(itemContainer);

    var title = item.name;
    if (isBook(item)) {
      var remark = JSON.parse(item.remark);
      title = remark['dpt'] + ' ' + remark['crs'];
    }

    var imgUrl = getItemImageUrl(item);
    var itemInfo = $('<div>').attr('class', 'item-info-wrapper')
      .append($('<img>').attr('class', 'item-image').attr('src', imgUrl))
      .append($('<div>').attr('class', 'item-name').text(title))
      .append(createPrice(item.price));
    var btn = $('<div>').attr('class', 'btn-add-container')
      .append($('<div>').addClass('bg'))
      .append($('<img>')
        .attr('class', 'btn-add')
        .attr('src', '/static/imgs/btn_add.png'));
    btn.click((function(id) {
      return function(e) { addToCart(id); e.stopPropagation(); }
    })(item.id));
    itemContainer.hover(
      function () {
        $(this).children('.btn-add-container').slideDown('fast');
      }, function () {
        $(this).children('.btn-add-container').slideUp('fast');
      });  
    itemContainer.append(itemInfo).append(btn);
    var wrapper = function() {
      // create a wrapper to store local item info in the loop
      var itemLocal = item;
      itemContainer.click(function() {
        $(document.body).append(ItemDetail.generate(itemLocal));
      });
    }();
  }
};

var showAd = function(store) {
  $('#ad').append($('<img>').attr('src', '{% static "imgs/" %}' + 'ad_' + store + '.png'));
}

var addToCart = function(itemId) {
  var cart;
  if (!$.cookie("cart")) {
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
	var size = !$.cookie("cart") ? 0 : JSON.parse($.cookie("cart")).length;
	if (size > 0) {
		$("#cart_bubble").show();
		$("#cart_bubble").children("p").text(size);
	}
}

var getAndShowItems = function(query, startId, num) {
  $.post('/home/getItems',
    {'startId' : startId, 'num' : num, 'query' : query}, 
    function(data) {
      if (data.length > 0) {
        // Assume no cross store query
        var store = data[0].store;
        generateItems(data, $('#item-list'), false);
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

var getPopularItems = function(query, startId, num) {
    $.post('/home/getPopularItems',
    {'startId' : startId, 'num' : num, 'query' : query}, 
    function(data) {
      if (data.length > 0) {
        // Assume no cross store query
        generateItems(data, $('#popular-item-list'), true);
      }
    }, 'json');
    $('#popular-item-list').fadeIn();
}

$(document).ready(function () {
  var query = getURLParameter('query');
  if (!query) {
    window.location = '/home/?query=store:sobeys';
  }
  updateCartBubble();
  var store = GetSelectedStore();
  showAd(store);
  getAndShowItems(query, 0, 12);
  $(".item-container").hover(function() {
    $(this).children(".btn-add-container").slideDown('fast');
  }, function () {
    $(this).children(".btn-add-container").slideUp('fast');
  });
  SearchBox.init();
  if (!isSearchResult())
    getPopularItems(query, 0, 4);
});
