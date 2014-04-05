angular.module('order.controllers', [
  'common.resources',
  'order.directive'
])
.controller('InvoiceDetail', [
  '$scope', '$q', 'InvoiceResource', 'OrderResource',
  function($scope, $q, InvoiceResource, OrderResource) {
    $scope.invoice = null;

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
