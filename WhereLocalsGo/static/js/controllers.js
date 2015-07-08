angular.module('starter.controllers', [])


.controller('MapCtrl', function($rootScope) {
    preferences=$rootScope.preferences;
    $rootScope.urlmap='/static/views/mapa.html?preferences=' + JSON.stringify(preferences);
    console.log('MapCtrl');
})

.controller('PlacesCtrl', function($scope, $rootScope, Places) {
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //

  console.log('PlacesCtrl');

 Places.all($rootScope,function(data, status) {
       $rootScope.Places=data;
 });

})

.controller('AccountCtrl', function($rootScope) {
    var d = new Date();
    var n = d.getDay();
    $rootScope.preferences.weekday=n;
    $rootScope.recomendme = function() {
        window.location='#/tab/map';
    };
});
