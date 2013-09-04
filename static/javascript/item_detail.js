var ItemDetail = function () {
	var isBook = function(item) {
  	return item.remark &&
         	 JSON.parse(item.remark) &&
         	 JSON.parse(item.remark)["crs"];
	};

	var generate = function (item) {
		$('.item-detail-container').remove(); 

		var imgUrl = 'http://108.171.244.148/static/sobeys_imgs/' + item.sku + '.JPG';
		var container = $('<div>').addClass('item-detail-container');
		var left = $('<div>').addClass('item-detail-container-left')
				.append($('<img>').addClass('item-detail-img').attr('src', imgUrl));
		var right = $('<div>').addClass('item-detail-container-right')
				.append($('<p>').addClass('item-detail-name').text(item.name))
				.append($('<p>').addClass('item-detail-price').text('Price: $' + item.price + ' CAD')
			);

		if (isBook(item)) {
			var remark = JSON.parse(item.remark);
			var bookInfoContainer = $('<div>').addClass('book-info-container');
			bookInfoContainer.append($('<p>').text('Course: ' + remark.dpt + ' ' + remark.crs));
			bookInfoContainer.append($('<p>').text('Author: ' + remark.author));
			bookInfoContainer.append($('<p>').text('Publisher: ' + remark.publisher));
			right.append(bookInfoContainer);
		}

		var addBtn = $('<img>')
        .attr('class', 'item-detail-btn-add')
        .attr('src', '/static/imgs/btn_add.png')
        .click(function() {
        	addToCart(item.id);
        	$(this).parent().parent().remove();
        });
    var cancelBtn = $('<img>')
        .attr('class', 'item-detail-btn-cancel')
        .attr('src', '/static/imgs/btn_cancel.png')
        .click(function () {
        	$(this).parent().parent().remove();
        });
		right.append(addBtn);
		right.append(cancelBtn);

		container.append(right);
		container.append(left);
		return container;
	};

	return {
		generate: generate
	};
}();