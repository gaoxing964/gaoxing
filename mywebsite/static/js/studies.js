if (window.location.search) {
    var searchItems = window.location.search.substring(1).split('&');
    var flag = false;
    var searchArrays = [];
    $.each(searchItems, function (index, item) {
        searchArrays.push(item.split('='));
    });
    $.each(searchArrays, function (index, item) {
        if (item[0] == 'blogTypeID') {
            window.currentBlogType = item[1];
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
            input = parseInt(input)*1000 ;
            var date = new Date(input);
            var year = date.getFullYear();
            var month = date.getMonth()+1;
            var day = date.getDate();
            return year + '-' + month + '-' + day;
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

    //分页
    $scope.totalCount = 1;
    $scope.currentPage = 1;
    $scope.pageSize = 5;
    $scope.currentBlogs = [];
    $http({
        type: 'get',
        'url': '/api/blogType/getAllBlogTypes'
    }).then(function (response) {
        if (response.status == 200) {
            $scope.blogTypes = angular.copy(response.data);
            window.blogTypes = angular.copy(response.data);
            console.log(window.blogTypes);
        }
    });

    //确定分页参数
    function exechangePage(pageIndex, blogTypeID) {
        if (!pageIndex) {
            $scope.currentPage = 1;
        } else {
            $scope.currentPage = pageIndex;
        }
        if (!blogTypeID) {
            blogTypeID = window.currentBlogType;
            if (!window.currentBlogType) {
                blogTypeID = 0;
            }
        }
        $scope.pages = [];

        $.ajax({
            type: 'POST',
            'url': 'api/getBlogByPage',
            data: {
                currentPage: $scope.currentPage,
                pageSize: $scope.pageSize,
                blogTypeID: blogTypeID
            },
            success: function (response) {
                $scope.$apply(function () {
                    response = eval('(' + response + ')');
                    $scope.currentBlogs = response.data;
                    $scope.totalCount = response.allCount;
                    $scope.maxPage = (function () {
                        if (($scope.totalCount) % $scope.pageSize) {
                            return parseInt(($scope.totalCount) / $scope.pageSize) + 1;
                        } else {
                            return parseInt(($scope.totalCount) / $scope.pageSize);
                        }
                    })();
                    $scope.firstIndex = (function () {
                        if ($scope.currentPage < 7) {
                            return 1;
                        } else if ($scope.currentBlogs > ( $scope.maxPage - 7)) {
                            return $scope.maxPage - 7;
                        } else {
                            return $scope.currentPage - 3;
                        }
                    })();
                    $scope.lastIndex = (function () {
                        if (($scope.maxPage < 7) || ( $scope.currentBlogs > ( $scope.maxPage - 7))) {
                            return $scope.maxPage;
                        } else {
                            return $scope.currentPage + 3;
                        }
                    })();
                    for (var i = $scope.firstIndex; i <= $scope.lastIndex; i++) {
                        $scope.pages.push(i);
                    }
                });
            }
        })

    }

    $scope.exechangePage = exechangePage;
    exechangePage(1);

    $http({
        type: 'get',
        url: '/api/getNewstBlogs'
    }).then(function (response) {
        if (response.status == 200) {
            $scope.newestBlogs = angular.copy(response.data);
        }
    });

    $http({
        type: 'get',
        url: '/api/getHotestBlogs'
    }).then(function (response) {
        if (response.status == 200) {
            $scope.hotestBlogs = angular.copy(response.data);
        }
    });

    $scope.exchangeBlogType = function (currentBlogType) {
        window.currentBlogType = currentBlogType;
        exechangePage(1, currentBlogType);
    };

});
