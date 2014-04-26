angular.module('shop', ['ui.router', 'shop.controllers'])
.config(function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise('/');

  $stateProvider
  .state('select', {
    url: '/',
    controller: 'StoreSelect',
    templateUrl: '/static/ng/shop/templates/store-select.html'
  })
  .state('home', {
    url: '/:slug',
    controller: 'StoreHome',
    templateUrl: '/static/ng/shop/templates/store-home.html'
  });
});
