angular.module('account.controllers', [
  'common.resources',
  'account.directive'
])
.controller('UserInvoices', [
  '$scope', '$q', 'FruitexAPI',
  function($scope, $q, FruitexAPI) {
    $scope.invoices = [];

    $scope.init = function(invoiceUrlBase) {
      FruitexAPI.current.invoices.get().$promise
      .then(function(response) {
        var invoices = $scope.invoices = response.results;
        _.each(invoices, function(invoice) {
          invoice.url = invoiceUrlBase + invoice.id;
          _.each(invoice.orders, function(orderId, i) {
            invoice.orders[i] = FruitexAPI.orders.get({ id: orderId });
          });
        });
      });
    };
  }
]);
