var OrderManager = function (orders, parent) {

  var createDeliveryInfo = function(order) {
    var container = $('<div>').addClass("delivery_info");
    container.append($("<p>").text("Status: " + order.status));
    container.append($("<p>").text("Created on: " + order.time));
    container.append($("<p>").text("Name: " + order.name));
    container.append($("<p>").text("Address: " + order.address));
    container.append($("<p>").text("Postcode: " + order.postcode));
    container.append($("<p>").text("Phone: " + order.phone));
    container.append($("<p>").text("Delivery Window: " + order.delivery_window));
    return container;
  }

  var createOrder = function(order) {
    var container =$("<div>").addClass('order-container');
    container.prepend($('<input>').val(order.invoice).attr('type', 'checkbox'));
    container.append(createDeliveryInfo(order));
    ItemList(order.items, false).generate(container); 
    return container;
  }

  var createOrderForAdmin = function (order) {
    var container = createOrder(order);
    var btn = $("<button>").text("Delivered!").click(function() {
      $.post('/orders/deliver',
        {
          'id': order.id,
          'status': "delivered"
        }, 
        function(data, err) {
          location.reload();
        }, 'json');
    })
    container.append(btn);
    return container; 
  }

  var generateCateList = function (cate, ids) {
    var container = $('<div>').append($('<p>').addClass('buy-list-title').text(cate));
    ItemList(ids, false).generate(container);
    $('#buy-list').append(container);
  }

  var generateBuyList = function () {
    var invoices = [];
    var checkedOrder = $('input:checkbox:checked');
    if (!checkedOrder.length) return;
    for (var i = 0; i < checkedOrder.length; i++) {
      invoices.push(checkedOrder[i].value);
    }
    $.post('/group_orders',
      {'invoices' : JSON.stringify(invoices)}, 
      function(data) {
        console.log(data);
        for (var i in data) {
          generateCateList(i, data[i])
        }
        $('#buy-list').show();
      }, 'json');
  };

  var init = function () {
    $('#btn-buy-list').click(function () {
      generateBuyList();
    })
    orders.reverse();
    for (i in orders) {
      parent.append(createOrderForAdmin(orders[i]));
    }
  };

  return {
    init: init,
    create: createOrder
  };

};
