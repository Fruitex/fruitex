var global = function () {
	var getUrlValue = function (key) {
		var res = {};
		var url = window.location.search.substr(1).split('\&');
		for (var i in url) {
			var pair = url[i].split('\=');
			res[pair[0]] = pair[1];
		}
    var s = decodeURIComponent(res[key]);
		return s;
	};

	var size = function (object) {
    	var size = 0;
    	for (var key in object) {
        	if (object.hasOwnProperty(key)) size++;
    	}	
    	return size;
	};
	return {
		getSize: size,
		getUrlValue: getUrlValue
	};
}();
