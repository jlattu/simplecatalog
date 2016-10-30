/**
 * Created by Lanttu on 28.10.2016.
 */

var catApp = angular.module('catApp', ['ngRoute']);

catApp.config(['$routeProvider',
     function($routeProvider) {
         $routeProvider.
             when('/', {
                 templateUrl: 'static/partials/shirts.html'
             }).
             otherwise({
                 redirectTo: '/'
             });
    }]);

catApp.controller('catalogCtrl', ['$scope', '$http', function ($scope, $http) {

    $scope.sortingKey = "name";
    $scope.sortingOrder = "asc";
    $scope.sortingLimit = 25;
    $scope.sortingOffset = 0;
    $scope.previousDisabled = true;
    $scope.nextDisabled = false;

    $scope.loadData = function () {
        $http.get('/get_shirts', {params: {sorting_key: $scope.sortingKey,
        sorting_order: $scope.sortingOrder, sorting_limit: $scope.sortingLimit,
        sorting_offset: $scope.sortingOffset}}).success(function(data){
            $scope.shirts = data;
           // console.log($scope.shirts);
        });
    };

    $scope.changeSortingKey = function (orderKey) {
        if ($scope.sortingKey == orderKey) {
            if ($scope.sortingOrder == "asc") $scope.sortingOrder = "desc";
            else $scope.sortingOrder = "asc";
        }
        else {
            $scope.sortingKey = orderKey;
            $scope.sortingOrder = "asc";
        }
        $scope.resetSortingOffset();
        $scope.loadData();
    };

    $scope.changeSortingLimit = function (sortingLimit) {
        $scope.sortingLimit = parseInt(sortingLimit);
        $scope.resetSortingOffset();
        $scope.loadData();
    };

    $scope.changeSortingOffset = function (change) {
        if (change == '-') {
            $scope.sortingOffset = $scope.sortingOffset - $scope.sortingLimit;
            if ($scope.sortingOffset <= 0) {
                $scope.resetSortingOffset();
            }
            else $scope.nextDisabled = false;
        }
        else {
            $scope.sortingOffset = $scope.sortingOffset + $scope.sortingLimit;
            $scope.previousDisabled = false;
            if ($scope.shirts.length < $scope.sortingLimit) $scope.nextDisabled = true;
        }
        $scope.loadData();
    };

    // Initial site load
    $scope.loadData();

    $scope.resetSortingOffset = function () {
        $scope.sortingOffset = 0;
        $scope.previousDisabled = true;
        $scope.nextDisabled = false;
    };

}]);
