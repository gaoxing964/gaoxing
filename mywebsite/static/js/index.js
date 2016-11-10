app = angular.module('myApp', []);
app.config(['$interpolateProvider', function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[');
	$interpolateProvider.endSymbol(']}');
}]);

app.filter('timeFormate', function() {
	return function(input) {
		if (input) {
			return input.substr(0, 4) + '-' + input.substr(4, 2) + '-' + input.substr(6, 2);
		}
	}
});
app.filter('blogTypeConfirm', function() {
	return function(input) {
		if (input && window.blogTypes) {
			var blogTypeTitle = '';
			$.each(window.blogTypes, function(index, item) {
				if ($.trim(input) == item.blogTypeID) {
					blogTypeTitle = item.blogTypeTitle;
				}
			});
			return blogTypeTitle;
		}
	}
});

app.filter('contentSubstr',function(){
	return function(input){
		if(input.length > 200){
			return input.substring(0,200)+'...';
		}else{
			return input ;
		}
	}
});
app.controller("myController", function($scope, $http) {

	$scope.images = ['../static/skatingImages/psb (1).jpg', '../static/skatingImages/psb (7).jpg', '../static/skatingImages/psb (9).jpg','../static/images/1-151220210P4.jpg'];

	$http({
		type: 'get',
		url: '/api/getNewstBlogs'
	}).then(function(response) {
		if (response.status == 200) {
			$scope.blogs = angular.copy(response.data);
		}
	});

	$http({
		type: 'get',
		url: '/api/getTopFiveRaiseBlogs'
	}).then(function(response) {
		if (response.status == 200) {
			$scope.raiseBlogs = angular.copy(response.data);
		}
	});

	$http({
		type: 'get',
		'url': '/api/blogType/getAllBlogTypes'
	}).then(function(response) {
		if (response.status == 200) {
			$scope.blogTypes = angular.copy(response.data);
			window.blogTypes = angular.copy(response.data);
		}
		console.log(window.blogTypes);
	});

});

$('#aChatWidthMe').click(function(){
	alert('请扫描微信二维码和我联系 ， 谢谢！');
});