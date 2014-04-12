angular.module('common.resources', ['ngResource'])
.service('FruitexAPI', function($resource){
  this.baseUrl = '/api';

  /* Invoices */
  this.invoices = $resource(this.baseUrl + '/invoices/:id',
    {id: '@id'},
    {'query': {method: 'GET', isArray: false }});

  /* Orders */
  this.orders = $resource(this.baseUrl + '/orders/:id', {id: '@id'});

  /* Users */
  this.users = $resource(this.baseUrl + '/users/:id', {id: '@id'});
});
