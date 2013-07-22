{% load static %}

function getCategoryId(s) {
  return 'cate-' + s.toLowerCase().replace(/[^a-z]/g, '');
}

function getCateHoverInHandler(c) {
  return function () {
    $('.sub-cate').hide();
    $('#' + getCategoryId(c)).show();
  };
}

function getCateHoverOutHandler() {
  return function () {
    $('.sub-cate').hide();
  };
}

function initCategory(cate, labels) {
  function getCateNum(c) {
    var res = 0;
    for (var sc in cate[c]) {
      res += cate[c][sc].length;
    }
    return res;
  }
  var cate_lst = $('<ul>').attr('id', 'cate-list');

  cate_lst.append($('<li>').attr('id', 'cate-head').text("Category"));
  for (var c in cate) {
    var label = $('<img>').attr('src', '{% static "imgs/" %}' + labels[c]);
    cate_lst.append($('<li>').attr('class', 'cate').append(label)
      .append($('<span>').text(c))
      .hover(getCateHoverInHandler(c), getCateHoverOutHandler()));
    var sub_cate = $('<div>').attr('class', 'sub-cate')
    .attr('id', getCategoryId(c)).hide()
    .hover(function(){$(this).show();}, function(){$(this).hide()});
    $('#category').append(sub_cate);
    var columnNum = Math.ceil(getCateNum(c)/15);
    var containers = [];
    sub_cate.css('width', ((150 + 8) * columnNum) + 'px');

    var cate_sub_header = $('<div>').attr('class', 'cate-sub-header').css('background-color', '#b4f943');
    sub_cate.append(cate_sub_header);

    for (var i = 0; i < columnNum ; i++) {
      var col = $('<div>').css({'float': 'left', 'width': '150px', 'height': '100%'});
      sub_cate.append(col);
      containers.push(col);
    }
    var idx = 0;
    for (var sc in cate[c]) {
      var cate_sub_lst = $('<ul>').attr('class', 'cate-sub-list');
      containers[idx].append(cate_sub_lst);
      idx = (idx + 1) % columnNum;
      cate_sub_lst.append($('<li>').attr('class', 'cate-sub-list-header').text(sc))
      for (var i in cate[c][sc]) {
        cate_sub_lst.append($('<li>')
          .attr('class', 'cate-sub-list-item')
          .text(cate[c][sc][i]));
      }
    }
  }
  $('#category').append(cate_lst);
}

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
  console.log($.cookie("cart"));
};

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
$(document).ready(function() { 
  var query = getURLParameter('query');
  getAndShowItems(query, 0, 12);
});
