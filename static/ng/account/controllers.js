angular.module('account.controllers', [
  'common.resources',
  'common.directive'
])
.controller('Invoices', [
  '$scope', '$q', 'InvoiceResource', 'OrderResource',
  function($scope, $q, InvoiceResource, OrderResource) {
    $scope.invoices = [];

    $scope.init = function(userId, username) {
      var invoices;

      InvoiceResource.query({ user__username: username }).$promise
      .then(function(response) {
        invoices = response.results;
        var orderPromises = _.flatten(_.map(invoices, function(invoice) {
          return _.map(invoice.orders, function(orderId, i) {
            var order = invoice.orders[i] = OrderResource.get({ id: orderId });
            return order;
          });
        }));

        return $q.all(orderPromises);
      })
      .then(function() {
        $scope.invoices = invoices;
      });
    };
  }
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
