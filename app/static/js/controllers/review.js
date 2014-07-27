'use strict';

angular.module('serveryApp')
.controller('ReviewCtrl', ['$scope','dishdetail', function($scope,dishdetail) {

    $scope.dishdetail = dishdetail;

}]);