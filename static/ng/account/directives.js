angular.module('common.directive', [])
  .directive('invoiceList', function() {
    return {
      templateUrl: '/static/ng/account/templates/invoice-list.html'
    };
  });
