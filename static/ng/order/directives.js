angular.module('order.directive', [])
.directive('ngInvoiceDetail', function() {
  return {
    scope: {
      invoice: '=ngInvoiceDetail'
    },
    controller: function($scope, $log) {
      $scope.allStatus = {
        'PEND': 'Pending',
        'PAID': 'Paid',
        'FLAG': 'Paid (Flagged)',
        'CANC': 'Cancelled',
        'POD': 'Pay on delivery'
      };
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
      $scope.allStatus = {
        'PEND': 'Pending',
        'WAIT': 'Waiting',
        'PURC': 'Purchased',
        'ONTW': 'On the way',
        'DELI': 'Delivered'
      };
    },
    templateUrl: '/static/ng/order/templates/order-status.html'
  };
})
.directive('ngOrderItemsTable', function() {
  return {
    scope: {
      orderItems: '=ngOrderItemsTable'
    },
    controller: function($scope, $log) {
      $scope.expanded = false;
      $scope.toggle = function() {
        $scope.expanded = !$scope.expanded;
      };
    },
    templateUrl: '/static/ng/order/templates/order-items-table.html'
  };
});
