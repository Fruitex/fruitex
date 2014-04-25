angular.module('store', ['store.controllers', 'ui.router'])
.run(function ($rootScope, $state, $stateParams) {
    $rootScope.$state = $state;
    $rootScope.$stateParams = $stateParams;
	}
)
.config(function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise('');


	$stateProvider
	.state("faq", {
		url: "/section/{section:\w+}",

		templateUrl: "/static/ng/store/templates/qa-section.html",
		controller: function($scope, $stateParams, $http) {
			var faq = $scope.$parent.faq;
			$scope.text = faq[$stateParams.section];
		}
	});
});