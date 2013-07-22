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
