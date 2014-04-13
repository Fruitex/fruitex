angular.module('order.controllers', [
  'common.resources',
  'order.directive'
])
.controller('InvoiceDetail', [
  '$scope', '$q', 'FruitexAPI',
  function($scope, $q, FruitexAPI) {
    $scope.authorize = function(email) {
      var result = email == $scope.invoice.email;
      if (result) { $scope.invoice.user = email; }
      return result;
    };

    $scope.init = function(invoiceId) {
      $scope.invoice = FruitexAPI.invoices.get({ id:invoiceId });
      $scope.invoice.$promise
      .then(function(invoice) {
        if (_.size(invoice) < 1) {
          // TODO: handle wrong response
          return;
        }

        _.each(invoice.orders, function(orderId, i) {
          invoice.orders[i] = FruitexAPI.orders.get({ id: orderId });
        });
      });
    };
  }
]);
