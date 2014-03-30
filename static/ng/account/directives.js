angular.module('common.directive', [])
.directive('ngInvoiceList', function() {
  return {
    scope: {
      invoices: '=ngInvoiceList'
    },
    templateUrl: '/static/ng/account/templates/invoice-list.html'
  };
})
.directive('ngInvoiceDetail', function() {
  return {
    scope: {
      invoice: '=ngInvoiceDetail'
    },
    templateUrl: '/static/ng/account/templates/invoice-detail.html'
  }
});
