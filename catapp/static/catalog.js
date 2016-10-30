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

    $scope.sortingKey = "id";
    $scope.sortingOrder = "asc";
    $scope.sortingLimit = 25;
    $scope.sortingOffset = 0;
    $scope.previousDisabled = true;
    $scope.nextDisabled = false;
    $scope.shirtSelected = {};

    $scope.shirtSizes = [
        {sizeID: 1, sizeName: 'XS'},
        {sizeID: 2, sizeName: 'S'},
        {sizeID: 3, sizeName: 'M'},
        {sizeID: 4, sizeName: 'L'},
        {sizeID: 5, sizeName: 'XL'},
        {sizeID: 6, sizeName: 'XXL'},
        {sizeID: 7, sizeName: 'XXXL'}
    ];
    $scope.defaultSelectedSize = $scope.shirtSizes[2].size;

    $scope.loadData = function () {
        $http.get('/get_shirts', {params: {sorting_key: $scope.sortingKey,
        sorting_order: $scope.sortingOrder, sorting_limit: $scope.sortingLimit,
        sorting_offset: $scope.sortingOffset}}).success(function(data){
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

    $scope.addNewShirt = function () {
        $http.post('/add_new_shirt', JSON.stringify($scope.newShirt)).then(function (response) {
            if (response.data) console.log(response);
            $scope.loadData();
        });
    };

    $scope.deleteShirt = function (shirt_id) {
        var deletingData = {"id": + shirt_id};
        $http.post('/delete_shirt', deletingData).then(function (response) {
            if (response.data) console.log(response);
            $scope.loadData();
        });
    };

    // Initial site load
    $scope.loadData();

    $scope.resetSortingOffset = function () {
        $scope.sortingOffset = 0;
        $scope.previousDisabled = true;
        $scope.nextDisabled = false;
    };



    // gets the template to ng-include for a table row / item
    $scope.getTemplate = function(shirt) {
        if (shirt.id === $scope.shirtSelected.id) return 'editShirt';
        else return 'displayShirt';
    };

    $scope.editShirt = function(shirt) {
        $scope.shirtSelected = angular.copy(shirt);
    };

    $scope.updateShirt = function(idx) {
        console.log("Saving contact");
        console.log($scope.shirtSelected);
        $http.post('/update_shirt', JSON.stringify($scope.shirtSelected)).then(function (response) {
            if (response.data) console.log(response);
        });
        $scope.shirts[idx] = angular.copy($scope.shirtSelected);
        $scope.resetEdit();
    };

        $scope.resetEdit = function() {
            $scope.shirtSelected = {};
        };


}]);
