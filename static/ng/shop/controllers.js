angular.module('shop.controllers', [
  'common.resources',
  'shop.directive'
])
.controller('StoreSelect', function($scope, FruitexAPI, $log) {
  FruitexAPI.stores.get().$promise
  .then(function(res) {
    $log.info('List of store loaded');
    $scope.stores = res.results;
  });
})
.controller('StoreHome', function($scope, $stateParams, FruitexAPI, $log){
  var store = {};
  var slug = $stateParams.slug;
  FruitexAPI.stores.query({ slug: slug }).$promise
  .then(function(res) {
    var stores = res.results;
    if (_.isEmpty(stores)) {
      $scope.error = "Unknown store name";
      return;
    }

    store = $scope.store = stores[0];
    $log.info('Store ' + store.name + ' loaded');
    return FruitexAPI.stores.categories.get({ id: store.id }).$promise;
  })
  .then(function(res) {
    $log.info('Store categories loaded');
    store.categories = res.results;
  });
});
