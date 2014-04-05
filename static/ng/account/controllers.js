angular.module('account.controllers', [
  'common.resources',
  'account.directive'
])
.controller('UserInvoices', [
  '$scope', '$q', 'InvoiceResource', 'OrderResource',
  function($scope, $q, InvoiceResource, OrderResource) {
    $scope.invoices = [];
    $scope.invoiceUrlBase = null;

    $scope.init = function(userId, username, invoiceUrlBase) {
      var invoices;

      InvoiceResource.query({ user__username: username }).$promise
      .then(function(response) {
        invoices = response.results;
        _.each(invoices, function(invoice) {
          invoice.url = invoiceUrlBase + invoice.id;
        });
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
]);
