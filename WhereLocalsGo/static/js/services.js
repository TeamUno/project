angular.module('starter.services', [])

.factory('Places', function($http) {
  // Might use a resource here that returns a JSON array


  return {
    all: function(callback) {
      var req = {
        method: 'POST',
        url: '/api/v1/places',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        data: 'email='
      };
      $http(req).success(callback);
    },
    get: function(chatId) {
      for (var i = 0; i < places.length; i++) {
        if (places[i].id === parseInt(chatId)) {
          return places[i];
        }
      }
      return null;
    }
  };
});
