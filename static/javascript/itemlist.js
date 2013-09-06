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
	  var imgUrl = getItemImageUrl(item);
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
	  var cost = count * item.price;
	  itemInfo.append($('<span>').attr('class', 'item-in-cart-price').text('$ ' + cost.toFixed(2)));
	  itemWrapper.append(itemInfo);
	  return itemWrapper;
	};

	var createItems = function(items, parent) {
	  for (var i = 0; i < items.length; i++) {
	    parent.append(
	    	createItem(items[i], 
	    	itemCountGetter(items[i].id))
	    );
	  }
	};

  var generate = function (parent, callback) {
  	var thisCopy = this;
	  $.post('/home/getItems',
	    {'ids' : JSON.stringify(itemIds)}, 
	    function(data) {
	      if (data.length > 0) {
	      	thisCopy.data = data;
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

	var updatePrice = function (spinner) {
		var price;
		for (var i = 0; i < this.data.length; i++) {
			if (this.data[i].id == spinner.id) {
				price = this.data[i].price;
				break;
			}
		}
		if (price) {
			var cost = $(spinner).val() * price;
			$(spinner).parent().parent().children('.item-in-cart-price')
					.text('$ ' + cost.toFixed(2));
		}
	}

	return {
		generate: generate,
		updatePrice: updatePrice
	};
};
