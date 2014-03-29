angular.module('common.resources', ['ngResource'])
  .factory('InvoiceResource', ['$resource', function( $resource ) {
    return $resource('/api/invoices/:id');
  }])
  .factory('OrderResource', ['$resource', function( $resource ) {
    return $resource('/api/orders/:id');
  }])
  .factory('UserResource', ['$resource', function( $resource ) {
    return $resource('/api/users/:id');
  }]);
