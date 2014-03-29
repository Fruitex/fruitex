angular.module('account.resources', ['ngResource'])
  .factory('UserInvoicesResource', ['$resource', function( $resource ) {
    return $resource('/api/invoices/?user__username=:username');
  }]);
