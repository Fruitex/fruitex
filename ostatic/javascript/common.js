function getURLParameter(name) {
  return decodeURIComponent(
      (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,''])[1]
  );
}
var RegExpFindAll = function (s, p, idx) {
  var r = new RegExp(p);
  var res = [];
  var match;
  while(match = r.exec(s)) {
    res.push(match[idx]);
  }
  return res;
};
var ParseQuery = function (query) {
  var storeP = /store:([^ ]*)/g;
  var stores = RegExpFindAll(query, storeP, 1);
  query = query.replace(storeP, '');
  var cateP = /cate:([^" ]+)/g;
  var cates = RegExpFindAll(query, cateP, 1);
  query = query.replace(cateP, '');
  cateP = /cate:"([^"]+)"/g;
  cates.push.apply(cates, RegExpFindAll(query, cateP, 1));
  query = query.replace(cateP, '');
  return {
    store: stores,
    cate: cates,
    keyword: query.replace(/^\s+|\s+$/, ''),
  };
};
var GetSelectedStore = function() {
  var curStore = ParseQuery(getURLParameter('query')).store[0];
  if (!curStore) {
    curStore = 'sobeys';
  }
  return curStore;
};

var GetSelectedStoreDisplay = function () {
  var store = GetSelectedStore();
  return store.substr(0, 1).toUpperCase() + store.substr(1);
}

var isIE = function(version, comparison){
    var $div = $('<div style="display:none;"/>').appendTo($('body'));
    $div.html('<!--[if '+(comparison||'')+' IE '+(version||'')+']><a>&nbsp;</a><![endif]-->');
    var ieTest = $div.find('a').length;
    $div.remove();
    return ieTest;
};

var getItemImageUrl = function(item) {
  return '/static/' + item.store + '_imgs/' + item.sku + '.JPG';
};

/*
 *  Google analytics code, don't touch.
 */
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-43781659-1', 'fruitex.ca');
ga('send', 'pageview');

