var ItemList = function (itemIds, editable,allow_sub_detail) {
	var itemCountGetter = function(id, ids) {
    var res = 0;
    for (var i = 0; i < itemIds.length; i++) {
      if (parseInt(itemIds[i]) == parseInt(id)) {
        res++;
      }
    }
    return res;
  };

	var createItem = function(item, count,allow_sub) {
	  var imgUrl = getItemImageUrl(item);
	  var itemWrapper = $('<div>').attr('class', 'item-in-cart')
	  	.append($('<img>').attr('class', 'item-in-cart-img').attr("src", imgUrl));
	  var itemInfo = $('<div>').attr('class', 'item-info-wrapper').append();
	  var item_info_left = $('<div>').addClass('item-info-left').append($('<span>').attr('class', 'item-in-cart-name').text(item.name)).append($('<span>').attr('class', 'item-in-cart-store').text("From: " + item.store));
	  itemInfo.append(item_info_left);
	  var allow_sub_dom = $('<label><input type="checkbox" checked data-id="' + item.id + '"/>Allow substitution</label>');
	  if (allow_sub !== null) {
	  	  allow_sub_dom.find('input').attr('disabled','disabled').prop('checked',allow_sub?true:false);
	  }
	  item_info_left.append(allow_sub_dom);
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

	var createItems = function(items, parent,allow_sub_detail) {
	  for (var i = 0; i < items.length; i++) {
	    if (typeof allow_sub_detail == 'undefined') {
	    	allow_sub = null;
	    }else{
	    	allow_sub = allow_sub_detail[items[i].id];
	    }
	    parent.append(
	    	createItem(items[i], 
	    	itemCountGetter(items[i].id),allow_sub)
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
	        createItems(data, parent,allow_sub_detail);
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
