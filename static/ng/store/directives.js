angular.module("store.directives", ["common.directives"])
.directive('ngAbout', function() {
	return {
		scope: {
			article: "=faq"
		},
		templateUrl: '/static/ng/store/templates/qa-item.html'
	};
});