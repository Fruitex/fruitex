angular.module('account.controllers', [
  'common.resources',
  'account.resources',
  'common.directive'
])
.controller('Invoices', [
  '$scope', '$q', 'UserResource', 'OrderResource', 'UserInvoicesResource',
  function($scope, $q, UserResource, OrderResource, UserInvoicesResource) {
    $scope.invoices = [];
    $scope.user = UserResource.get({ id: 'current' });

    var invoices;

    $scope.user.$promise
      .then(function(user) {
        return UserInvoicesResource.get({ username: user.username }).$promise;
      })
      .then(function(raw) {
        invoices = raw.results;
        var orderPromises = [];

        invoices.forEach(function(invoice) {
          invoice.orders.forEach(function(orderId, i) {
            var order = OrderResource.get({ id: orderId });
            invoice.orders[i] = order;
            orderPromises.push(order.$promise);
          });
        });
        return $q.all(orderPromises);
      })
      .then(function() {
        $scope.invoices = invoices;
      });
  }
]);
