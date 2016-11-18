if (window.location.search) {
	var searchItems = window.location.search.substring(1).split('&');
	var flag = false;
    var searchArrays = [] ;
	$.each(searchItems, function(index, item) {
        searchArrays.push(item.split('='));
	});
    $.each(searchArrays , function(index,item){
        if(item[0] == 'blogID'){
            window.currentBlog = item[1];
        }
    });
}

/**
 * Created by teng.gao on 2016/5/18.
 */
app = angular.module('myApp', []);
app.config(['$interpolateProvider', function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
}]);

app.filter('timeFormate', function () {
    return function (input) {
        if (input) {
            return input.substr(0, 4) + '-' + input.substr(4, 2) + '-' + input.substr(6, 2);
        }
    }
});

app.filter('blogTypeConfirm', function () {
    return function (input) {
        if (input && window.blogTypes) {
            var blogTypeTitle = '';
            $.each(window.blogTypes, function (index, item) {
                if ($.trim(input) == item.blogTypeID) {
                    blogTypeTitle = item.blogTypeTitle;
                }
            });
            return blogTypeTitle;
        }
    }
});

app.controller("myController", function ($scope, $http) {


});

