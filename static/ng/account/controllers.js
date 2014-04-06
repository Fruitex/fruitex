angular.module('account.controllers', [
  'common.resources',
  'account.directive'
])
.controller('UserInvoices', [
  '$scope', '$q', 'InvoiceResource', 'OrderResource',
  function($scope, $q, InvoiceResource, OrderResource) {
    $scope.invoices = [];

    $scope.init = function(userId, username, invoiceUrlBase) {
      InvoiceResource.query({ user__username: username }).$promise
      .then(function(response) {
        var invoices = $scope.invoices = response.results;
        _.each(invoices, function(invoice) {
          invoice.url = invoiceUrlBase + invoice.id;
          _.each(invoice.orders, function(orderId, i) {
            invoice.orders[i] = OrderResource.get({ id: orderId });
          });
        });
      });
    };
  }
]);
