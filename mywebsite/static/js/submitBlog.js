if (window.location.search) {
    var searchItems = window.location.search.substring(1).split('&');
    var flag = false;
    var searchArrays = [];
    $.each(searchItems, function (index, item) {
        searchArrays.push(item.split('='));
    });
    $.each(searchArrays, function (index, item) {
        if (item[0] == 'blogID') {
            window.currentBlog = item[1];
        }
    });
}

window.contentType = 'HTML';


app = angular.module('myApp', []);
app.config(['$interpolateProvider', function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
}]);


app.controller("myController", function ($scope, $http, $timeout) {

    var blog = {
        blogID: '',
        blogTypeID: '',
        blogTitle: '',
        blogContent: '',
        puhlishTime: '',
        blogKeyWords: '',
        blogDescription: '',
        raiseFlag: 0
    }


    $http({
        type: 'get',
        'url': '/api/blogType/getAllBlogTypes'
    }).then(function (response) {
        if (response.status == 200) {
            $scope.blogTypes = angular.copy(response.data);
            window.blogTypes = angular.copy(response.data);
            $timeout(function () {
                if (window.operationType == 'MOD') {
                    $scope.blog = angular.copy(window.blog);
                } else {
                    $scope.blog = angular.copy(blog);
                }
            }, 100);

        }
    });

    $scope.submibBlog = function () {

        var url = '/submitBlog';
        callBack = function (response) {
            alert(response.message);
        };

        $scope.blog.blogContent = (function () {
            return $('#blogContent').val();
        })();

        $scope.blog.blogDescription = (function(){
            return $scope.blog.blogDescription.replace(/[\r\n\s]/g,'');
        })();

        if (window.operationType == 'MOD') {
            url = '/api/modifyBlog';
        }

        $.ajax({
            type: 'post',
            url: url,
            data: $scope.blog
        }).success(function (response) {
            response = eval('(' + response + ')');
            callBack(response);
        });
    }

    $scope.preview = function(){
          $scope.blog.blogContent = (function () {
            return $('#blogContent').val();
          })();

    }


});

$(document).ready(function () {


})
