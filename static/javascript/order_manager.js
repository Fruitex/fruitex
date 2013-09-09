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
  console.log(order);
  var container =$("<div>").addClass('order-container');
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
