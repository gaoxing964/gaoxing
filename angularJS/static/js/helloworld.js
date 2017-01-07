var myApp = angular.module("myApp", ['ui.router']);

myApp.config(function($stateProvider, $urlRouterProvider) {

	$urlRouterProvider.when("", "/page1");

	$stateProvider
		.state("page1", {
			url: "/page1",
			templateUrl: "Page_1"
		})
		.state("page2", {
			url: "/page2",
			templateUrl: "Page_2"
		})
		.state("page3", {
			url: "/page3",
			templateUrl: "Page_3"
		});
});