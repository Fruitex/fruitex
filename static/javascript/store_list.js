{% load static %}
var StoreList = function () {
	var init = function () {
		$('#store-list').children('li:not(:first-child)').click(function () {
			window.location = '/home/?store=' + $(this).attr('id');
		})
		var curStore = getURLParameter('store') ? getURLParameter('store') : 'sobeys';
		if ($('#store-list').children('#' + curStore)) {
			$('#store-list').children('#' + curStore).append(
				$('<img>')
					.addClass('store-list-green-dot')
					.attr('src', '{% static "imgs/green_dot.png" %}')
			);
		};
	};

	return {
		init: init
	};
}();

$(document).ready(function () {
	StoreList.init();
})