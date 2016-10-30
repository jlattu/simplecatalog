/**
 * Created by Lanttu on 28.10.2016.
 */

var catApp = angular.module('catApp', ['ngRoute']);

catApp.config(['$routeProvider',
     function($routeProvider) {
         $routeProvider.
             when('/', {
                 templateUrl: 'static/partials/shirts.html',
             }).
             otherwise({
                 redirectTo: '/'
             });
    }]);

catApp.controller('catalogCtrl', ['$scope', '$http', function ($scope, $http) {

    $scope.sortingKey = "color";
    $scope.sortingOrder = "asc";

    $scope.loadData = function () {
        $http.get('/get_shirts', {params: {sorting_key: $scope.sortingKey,
        sorting_order: $scope.sortingOrder}}).success(function(data){
            $scope.shirts = data;
            console.log($scope.shirts);
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

    // Initial site load
    $scope.loadData();


}]);
