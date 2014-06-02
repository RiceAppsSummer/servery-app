'use strict'

angular.module('serveryApp')
.controller('LoginController',
                ['$scope','User',"$location",function($scope,User,$location) {

    $scope.user = User.current_user();
    console.log($scope.user);

    $scope.logout = function()
    {
        User.logout(function()
        {
            $scope.user = None
        });
    };

}]);


angular.module('serveryApp')
.controller('MainCtrl', 
  ['$scope', 'Servery', 'Menu','User', function ($scope, Servery, Menu,User) {

  /*=============================================*
   * Servery selector
   *=============================================*/
  $scope.serveries = Servery.all(function () {
    // Once serveries are loaded
    if ($scope.serveries.length > 0)
      $scope.selectServery($scope.serveries[0]);
    else
      console.log('No serveries found');
  });

  $scope.selectServery = function (servery) {
    // Load servery details
    $scope.servery = Servery.query({'serveryId': servery.id},
      function() {
        console.log($scope.servery); // Log to console once loaded
      });

    // Load menu
    $scope.menu = Menu.query({'serveryId': servery.id, 'date': $scope.datePicker.dt.toISOString()},
      function() {
        console.log($scope.menu);   // Log to console once loaded
      });

    console.log("Selected servery: " + servery.name);
    console.log(servery);


    $scope.user = User.current_user();
    console.log($scope.user)
  };

  $scope.meals = ['breakfast', 'lunch', 'dinner'];

  /*=============================================*
   * Date picker
   *=============================================*/
  // Settings for the date picker
  $scope.datePicker = {
    today: function () {
      $scope.datePicker.dt = new Date();
    },
    open: function($event) {
      $event.preventDefault();
      $event.stopPropagation();
      $scope.opened = true;
    },
    dateOptions: {
      'year-format': "'yy'",
      'starting-day': 0
    },
  };

  $scope.$watch('datePicker.dt', function () {

    if ($scope.servery)
    $scope.menu = Menu.query({'serveryId': $scope.servery.id,'date':$scope.datePicker.dt.toISOString()});
  });

  // Initialize the datePicker to today
  $scope.datePicker.today();

}]);

