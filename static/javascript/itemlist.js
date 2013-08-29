var ItemList = function (itemIds, editable) {

	var itemCountGetter = function(id, ids) {
    var res = 0;
    for (var i = 0; i < itemIds.length; i++) {
      if (parseInt(itemIds[i]) == parseInt(id)) {
        res++;
      }
    }
    return res;
  };

	var createItem = function(item, count) {
	  var imgUrl = 'http://108.171.244.148/static/sobeys_imgs/' + item.sku + '.JPG';
	  var itemWrapper = $('<div>').attr('class', 'item-in-cart')
	  	.append($('<img>').attr('class', 'item-in-cart-img').attr("src", imgUrl));
	  var itemInfo = $('<div>').attr('class', 'item-info-wrapper')
	  	.append($('<div>').addClass('item-info-left')
	    	.append($('<span>').attr('class', 'item-in-cart-name').text(item.name))
	    	.append($('<span>').attr('class', 'item-in-cart-store').text("From: " + item.store))
	    );
	  if (editable) {
	    itemInfo.append($('<input>').attr('class', 'num-spinner')
	    	.attr('value', count).attr('id', item.id));
	  } else {
	  	itemInfo.append($('<span>').attr('class', 'item-in-cart-count').text('Quatity: ' + count).attr('id', item.id));
	  }
	  itemInfo.append($('<span>').attr('class', 'item-in-cart-price').text('$ ' + count * item.price))
	  itemWrapper.append(itemInfo);
	  return itemWrapper;
	};

	var createItems = function(items, parent) {
		console.log(parent);
	  for (var i = 0; i < items.length; i++) {
	    parent.append(
	    	createItem(items[i], 
	    	itemCountGetter(items[i].id))
	    );
	  }
	};

  var generate = function (parent, callback) {
	  $.post('/home/getItems',
	    {'ids' : JSON.stringify(itemIds)}, 
	    function(data) {
	    	console.log(data);
	      if (data.length > 0) {
	        createItems(data, parent);
	        if (callback)
	        	callback();
	      }
	      $('.num-spinner').spinner({
	        min: 0,
	        max: 100,
	        step: 1,
	      });
	    }, 'json');
	};

	return {
		generate: generate
	};
};