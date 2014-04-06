angular.module('order.controllers', [
  'common.resources',
  'order.directive'
])
.controller('InvoiceDetail', [
  '$scope', '$q', 'InvoiceResource', 'OrderResource',
  function($scope, $q, InvoiceResource, OrderResource) {
    $scope.authorize = function(email) {
      var result = email == $scope.invoice.email;
      if (result) { $scope.invoice.user = email; }
      return result;
    };

    $scope.init = function(invoiceId) {
      $scope.invoice = InvoiceResource.get({ id:invoiceId });
      $scope.invoice.$promise
      .then(function(invoice) {
        if (_.size(invoice) < 1) {
          // TODO: handle wrong response
          return;
        }

        _.each(invoice.orders, function(orderId, i) {
          invoice.orders[i] = OrderResource.get({ id: orderId });
        });
      });
    };
  }
]);
