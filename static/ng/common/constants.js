angular.module('common.constants', [])
.service('FruitexConstants', function(){
  /* Invoices */
  this.invoices = {
    statusList: [
      ['PEND', 'Pending'],
      ['PAID', 'Paid'],
      ['FLAG', 'Paid (Flagged)'],
      ['CANC', 'Cancelled'],
      ['POD', 'Pay on delivery']
    ]
  };
  this.invoices.status = _.object(this.invoices.statusList);

  /* Orders */
  this.orders = {
    statusList: [
      ['PEND', 'Pending'],
      ['WAIT', 'Submitted'],
      ['PURC', 'Purchased'],
      ['ONTW', 'On the way'],
      ['DELI', 'Delivered']
    ]
  };
  this.orders.status = _.object(this.orders.statusList);
});
