'use strict';

angular.module('serveryApp')
.controller('UserSettingsCtrl', ['$scope','User', function($scope,User) {

    $scope.test = "foo";
    $scope.user = User.current_user(function()
    {
    });
    

}]);