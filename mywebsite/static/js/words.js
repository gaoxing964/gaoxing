/**
 * Created by teng.gao on 2016/5/21.
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

app.controller("myController", function ($scope, $http) {


    $scope.totalCount = 1;
    $scope.currentPage = 1;
    $scope.pageSize = 5;
    $scope.currentWords = [];
    $scope.raiseWords = [];
    $scope.currentSubWords = [];

    $scope.wordSubmit = {
        'wordsContent': '',
        parentsID: '0'
    }

    $scope.wordSubmitSub = {
        'wordsContent': '',
        parentsID: '0'
    }

    $http({
        'type': 'get',
        'url': '/api/getRaiseWords'
    }).then(function (response) {
        $scope.raiseWords = response.data;
    });
    //ȷ����ҳ����
    function exechangePage(pageIndex, field, direction) {
        if (!pageIndex) {
            $scope.currentPage = 1;
        } else {
            $scope.currentPage = pageIndex;
        }
        if (!field) {
            if (window.field) {
                field = window.field;
            } else {
                field = 'publishTime'
            }
        }
        if (!direction) {
            if (window.direction) {
                direction = window.direction;
            } else {
                direction = 'desc';
            }
        }
        $scope.pages = [];
        $http({
            type: 'get',
            url: 'api/getWordsByPage/' + $scope.currentPage + '/' + $scope.pageSize + '/' + field + '/' + direction
        }).then(function (response) {
            console.log(response);
            var wordIds = [];
            $scope.currentWords = response.data.data;
            $scope.totalCount = response.data.totalCount[0]
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
            $.each($scope.currentWords, function (index, itemSub) {
                wordIds.push(itemSub['wordsId']);
            });
            wordIds = wordIds.join(',');
            $http({
                type: 'get',
                url: '/api/getSubWords/' + wordIds
            }).then(function (response) {
                $scope.currentSubWords = response.data;
                console.log($scope.currentSubWords);
            });

        });
    }

    $scope.exechangePage = exechangePage;
    exechangePage(1);

    $scope.orderByExchange = function (field, direction) {
        window.field = field;
        window.direction = direction;
        exechangePage(1, field, direction);
    }

    $scope.submitWord = function () {
        $http({
            type: 'get',
            'url': '/api/submitWord/' + $scope.wordSubmit.wordsContent + '/' + $scope.wordSubmit.parentsID
        }).then(function (response) {
            if (response.data.status == 200) {
                exechangePage(1);
                $scope.wordSubmit = {
                    'wordsContent': '',
                    parentsID: '0'
                }
            }
        });
    }


    $scope.replayWord = function (replayWord) {


        $('.subLeftWordsCommit').filter(function () {
            if ($(this).attr('wordId') != replayWord.wordsId) {
                return true;
            }
        }).slideUp();
        $('.subLeftWordsCommit').filter(function () {
            if ($(this).attr('wordId') == replayWord.wordsId) {
                return true;
            }
        }).slideToggle();
        $scope.wordSubmitSub.parentsID = replayWord.wordsId;

    }

    $scope.submitSubWord = function () {
        $http({
            type: 'get',
            'url': '/api/submitWord/' + $scope.wordSubmitSub.wordsContent + '/' + $scope.wordSubmitSub.parentsID
        }).then(function (response) {
            if (response.data.status == 200) {
                exechangePage(1);
                $scope.wordSubmitSub = {
                    'wordsContent': '',
                    parentsID: '0'
                }
            }
        });
    }


});