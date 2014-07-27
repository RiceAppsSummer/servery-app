'use strict';

angular.module('serveryApp', ['ui.bootstrap', 'serveryApi', 'serveryFilters','userApi','ngRoute'])
  .config(function ($routeProvider) {

    $routeProvider
      .when('/', {
        templateUrl: 'static/views/main.html',
        controller: 'MainCtrl',
        resolve: {
          serveries: ['Servery','$q', function(Servery,$q) { 
            var defered = $q.defer();

            Servery.all(function(result)
            {
              defered.resolve(result.serveries);
            });

            return defered.promise;
          }]
        }
      })
      .when('/userSettings', {
        templateUrl: 'static/views/userSettings.html',
        controller: 'UserSettingsCtrl'
      })
      .when('/quickView', {
        templateUrl: 'static/views/quickView.html',
        controller: 'QuickViewCtrl',
        resolve: {
          nextmeals: ['Servery','$q', function(Servery,$q) {
            var defered = $q.defer();

            Servery.nextMeals(function(result)
            {
              defered.resolve(result);
            });
            return defered.promise;
          }]
        }
      })

      .when('/review/:dishdetailsId', {
        templateUrl: 'static/views/reviewPage.html',
        controller: 'ReviewCtrl',
        resolve: {
          dishdetail: ['DishDetails','$q','$route', function(DishDetails,$q,$route) {
            var defered = $q.defer();

            DishDetails.query({dishdetailsId:$route.current.params.dishdetailsId},function(result)
            {
              defered.resolve(result);
            });
            return defered.promise;
          }]
        }
      })

      .when('/search', {
        templateUrl: 'static/views/search.html'
      })
     
      .otherwise({
        redirectTo: '/'
      });
  });
