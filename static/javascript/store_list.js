{% load static %}
var StoreList = function () {
	var init = function () {
		$('#store-list').children('li:not(:first-child)').click(function () {
			window.location = '/home/?query=' + 'store:' + $(this).attr('id');
		})
		var curStore = ParseQuery(getURLParameter('query')).store[0];
    if (!curStore) {
      curStore = 'sobeys';
    }
    SelectCurrentStoreUI(curStore);
	};

	return {
		init: init
	};
}();

var SelectCurrentStoreUI = function (curStore) {
  if ($('#store-list').children('#' + curStore)) {
    $('#store-list').children('#' + curStore).append(
      $('<img>')
        .addClass('store-list-green-dot')
        .attr('src', '{% static "imgs/green_dot.png" %}')
    );
  };
}

$(document).ready(function () {
	StoreList.init();
})
