angular.module('account.directive', ['common.constants'])
.directive('ngInvoiceRow', function(FruitexConstants) {
  return {
    scope: {
      invoice: '=ngInvoiceRow'
    },
    controller: function($scope, $log) {
      $scope.orderStatus = FruitexConstants.orders.status;
    },
    templateUrl: '/static/ng/account/templates/invoice-row.html'
  };
});
