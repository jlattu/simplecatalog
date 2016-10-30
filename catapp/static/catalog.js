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

    $scope.sortingKey = "color";
    $scope.sortingOrder = "asc";
    $scope.sortingLimit = 25;

    $scope.loadData = function () {
        $http.get('/get_shirts', {params: {sorting_key: $scope.sortingKey,
        sorting_order: $scope.sortingOrder, sorting_limit: $scope.sortingLimit}}).success(function(data){
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
        $scope.loadData();
    };

    $scope.changeSortingLimit = function (sortingLimit) {
        $scope.sortingLimit = sortingLimit;
        $scope.loadData();
    };

    // Initial site load
    $scope.loadData();

}]);
