/*global todomvc */
'use strict';

/**
 * Services that provide access to the servery API. 
 */
angular.module('serveryApp').factory('Api', function ($http, $q) {

  return {

    /**
     * Returns a deferred list of serveries.
     */
    serveries: function () {
      var deferred = $q.defer();

      // $http.get('/api/serveries').success(function (data) {
      //   deferred.resolve(data);
      // });
      deferred.reject('Not implemented');

      return deferred.promise;
    }
    
  };

});