function getURLParameter(name) {
    return decodeURI(
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
  var cateP = /cate:([^' ]+)/g;
  var cates = RegExpFindAll(query, cateP, 1);
  query = query.replace(cateP, '');
  cateP = /cate:'([^']+)'/g;
  cates.push.apply(cates, RegExpFindAll(query, cateP, 1));
  query = query.replace(cateP, '');
  return {
    store: stores,
    cate: cates,
    keyword: query.replace(/^\s+|\s+$/, ''),
  };
};
