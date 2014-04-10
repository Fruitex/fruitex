angular.module('order.directive', ['common.directives'])
.directive('ngInvoiceGuestAuth', function() {
  return {
    scope: {
      authorize: '&ngInvoiceGuestAuth'
    },
    controller: function($scope, $log) {
      $scope.auth = function() {
        if (!$scope.authorize({ email: $scope.email})) {
          $scope.error = "The email you entered is incorrect. ";
        }
      };
      $scope.change = function() { $scope.error = undefined; };
    },
    templateUrl: '/static/ng/order/templates/invoice-guest-auth.html'
  };
})
.directive('ngInvoiceDetail', function() {
  return {
    scope: {
      invoice: '=ngInvoiceDetail'
    },
    controller: function($scope, $log) {
      $scope.statusList = [
        ['PEND', 'Pending'],
        ['PAID', 'Paid'],
        ['FLAG', 'Paid (Flagged)'],
        ['CANC', 'Cancelled'],
        ['POD', 'Pay on delivery']
      ];
      $scope.allStatus = _.object($scope.statusList);
    },
    templateUrl: '/static/ng/order/templates/invoice-detail.html'
  };
})
.directive('ngOrderDetail', function() {
  return {
    scope: {
      order: '=ngOrderDetail'
    },
    templateUrl: '/static/ng/order/templates/order-detail.html'
  };
})
.directive('ngOrderStatus', function() {
  return {
    scope: {
      status: '=ngOrderStatus'
    },
    controller: function($scope, $log) {
      $scope.statusList = [
        ['PEND', 'Pending'],
        ['WAIT', 'Waiting'],
        ['PURC', 'Purchased'],
        ['ONTW', 'On the way'],
        ['DELI', 'Delivered']
      ];
      $scope.allStatus = _.object($scope.statusList);
    },
    templateUrl: '/static/ng/order/templates/order-status.html'
  };
})
.directive('ngOrderItems', function() {
  return {
    scope: {
      orderItems: '=ngOrderItems'
    },
    controller: function($scope, $log) {
      $scope.expanded = false;
      $scope.toggle = function() {
        $scope.expanded = !$scope.expanded;
      };
    },
    templateUrl: '/static/ng/order/templates/order-items.html'
  };
});
