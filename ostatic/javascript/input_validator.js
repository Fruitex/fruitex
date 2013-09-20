var InputValidator = function () {

	var init = function () {
		$('.input-validator-error-msg').remove();
		$('input').removeClass('input-validator-error-input');
	}

	var T = function (field, test, errMsg) {
		var showError = function() {
			field.addClass('input-validator-error-input');
			field.parent().append($('<span>').text(errMsg).addClass('input-validator-error-msg'));
		};
		if (!test(field.val())) {
			showError();
			return false;
		}
		return true;
	}

	var isValidEmail = function (email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
	};

	var isValidPhoneNumber = function (phone) {
		var re = /^[(]{0,1}[0-9]{3}[)]{0,1}[-\s\.]{0,1}[0-9]{3}[-\s\.]{0,1}[0-9]{4}$/;
		return re.test(phone);
	};

	var isNotEmpty = function (input) {
		return input.length > 0;
	};

	var isValidZIP = function (zip) {
		var re = /^[A-Za-z][0-9][A-Za-z]\s{0,1}[0-9][A-Za-z][0-9]$/;
		return re.test(zip);
	};

	return {
		init: init,
		email: function (input) { return T(input, isValidEmail, "invalid email format"); },
		phone: function (input) { return T(input, isValidPhoneNumber, "invalid phone number"); },
		nonEmpty: function (input) { return T(input, isNotEmpty, "cannot be blank"); },
		zip: function (input) { return T(input, isValidZIP, "invalid zip"); }
	};
}();