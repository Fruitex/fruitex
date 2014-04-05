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
});
