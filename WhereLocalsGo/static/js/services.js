angular.module('starter.services', [])

.factory('Places', function($http) {
  // Might use a resource here that returns a JSON array
  return {
    all: function(rootScope,callback) {
      console.log(JSON.stringify(rootScope.preferences));
      var req = {
        method: 'POST',
        url: '/api/v1/places',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        data: rootScope.preferences //'category=' + rootScope.preferences.category +'&age=' + rootScope.preferences.age +'&gender=' + rootScope.preferences.gender +'&amount=' + rootScope.preferences.amount
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
