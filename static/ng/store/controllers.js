angular.module('store.controllers', [
  'common.resources',
  'store.directives'
])
.controller('FruitexFaq', [
  '$scope', '$q', '$http',
  function($scope, $q, $http) {
    $scope.faq = {};

    $scope.init = function() {
	    $http.get('/static/ng/store/faq.json')
		    .then(function(res) {
			    var faqlist = res.data;
			    $.each(faqlist, function(idx, elem) {
				    $scope.faq[elem.section] = elem;
			    });
		    });
    };
  }
]).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});
