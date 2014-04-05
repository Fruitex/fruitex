angular.module('common.resources', ['ngResource'])
  .factory('InvoiceResource', ['$resource', function( $resource ) {
    return $resource('/api/invoices/:id', {id: '@id'},
      {'query': {method: 'GET', isArray: false }});
  }])
  .factory('OrderResource', ['$resource', function( $resource ) {
    return $resource('/api/orders/:id', {id: '@id'});
  }])
  .factory('UserResource', ['$resource', function( $resource ) {
    return $resource('/api/users/:id', {id: '@id'});
  }]);
