angular.module('common.resources', ['ngResource'])
.service('FruitexAPI', function($resource){
  this.baseUrl = '/api';

  /* Stores */
  this.stores = $resource(this.baseUrl + '/stores/:id',
    {id: '@id'},
    {'query': {method: 'GET', isArray: false }});
  this.stores.categories = $resource(this.baseUrl + '/stores/:id/categories', {id: '@id'});

  /* Invoices */
  this.invoices = $resource(this.baseUrl + '/invoices/:id',
    {id: '@id'},
    {'query': {method: 'GET', isArray: false }});

  /* Orders */
  this.orders = $resource(this.baseUrl + '/orders/:id', {id: '@id'});

  /* Users */
  this.users = $resource(this.baseUrl + '/users/:id', {id: '@id'});

  /* Current user */
  this.current = $resource(this.baseUrl + '/users/current');
  this.current.invoices = $resource(this.baseUrl + '/users/current/invoices');
});
