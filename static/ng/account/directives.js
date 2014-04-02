angular.module('common.directive', [])
.directive('ngInvoiceRow', function() {
  return {
    scope: {
      invoice: '=ngInvoiceRow'
    },
    templateUrl: '/static/ng/account/templates/invoice-row.html'
  };
})
.directive('ngInvoiceDetail', function() {
  return {
    scope: {
      invoice: '=ngInvoiceDetail'
    },
    templateUrl: '/static/ng/account/templates/invoice-detail.html'
  };
});
