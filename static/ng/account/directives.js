angular.module('account.directive', [])
.directive('ngInvoiceRow', function() {
  return {
    scope: {
      invoice: '=ngInvoiceRow'
    },
    templateUrl: '/static/ng/account/templates/invoice-row.html'
  };
});
