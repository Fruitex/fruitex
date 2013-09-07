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

function newQuery(cate, store) {
  return 'cate:"' + cate + '"' + ' store:' + store;
}

function initCategory(cate, labels) {
  function getCateNum(c) {
    var res = 0;
    for (var sc in cate[c]) {
      res += cate[c][sc].length;
    }
    return res;
  }

  var sortedCate = [];
  for (var c in cate) {
    sortedCate.push(c);
  }
  sortedCate.sort(function (a, b) {
    return global.getSize(cate[a]) < global.getSize(cate[b]);
  });
  var cate_lst = $('<ul>').attr('id', 'cate-list');
  cate_lst.append($('<li>').attr('id', 'cate-head').text("Category"));
  var index = 0;
  for (var j = 0; j < sortedCate.length; j++) {
    var c = sortedCate[j];
    var label = $('<img>').attr('src', '{% static "imgs/" %}' + labels[c]);
    cate_lst.append($('<li>').attr('class', 'cate').append(label)
        .append($('<span>').text(c))
        .hover(getCateHoverInHandler(c), getCateHoverOutHandler()));
    var sub_cate = $('<div>').attr('class', 'sub-cate')
        .attr('id', getCategoryId(c)).hide()
        .hover(function(){$(this).show();}, function(){$(this).hide()});
    $('#category').append(sub_cate);
    var columnNum = Math.ceil((0.1 + getCateNum(c))/15.0);
    var containers = [];
    sub_cate.css('width', ((150 + 8) * columnNum) + 'px');
    sub_cate.css('top', 50 * index + 'px');
    var cate_sub_header = $('<div>').attr('class', 'cate-sub-header').css('background-color', '#b4f943');
    sub_cate.append(cate_sub_header);

    for (var i = 0; i < columnNum ; i++) {
      var col = $('<div>').css({'float': 'left', 'width': '150px', 'height': '100%'});
      sub_cate.append(col);
      containers.push(col);
    }
    var idx = 0;
    var sorted_subcate = [];
    for (var sc in cate[c]) {
      sorted_subcate.push(sc);
    }
    sorted_subcate.sort();
    for (var k in sorted_subcate) {
      var sc = sorted_subcate[k];
      var cate_sub_lst = $('<ul>').attr('class', 'cate-sub-list');
      containers[idx].append(cate_sub_lst);
      idx = (idx + 1) % columnNum;
      cate_sub_lst.append($('<li>').append(
            $('<a>').attr('class', 'cate-sub-list-header')
            .attr('href', '/home/?query=' + encodeURIComponent(newQuery(sc, GetSelectedStore())))
            .text(sc)));
      for (var i in cate[c][sc]) {
        var s = cate[c][sc][i];
        cate_sub_lst.append($('<li>').append(
              $('<a>').attr('class', 'cate-sub-list-item')
              .attr('href', '/home/?query=' + encodeURIComponent(newQuery(sc + '->' + s, GetSelectedStore())))
              .text(s)));
      }
    }
    index += 1;
  }
  $('#category').append(cate_lst);
}
