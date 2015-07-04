angular.module('starter.controllers', [])


.controller('MapCtrl', function($rootScope) {

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
    $rootScope.recomendme = function() {
        window.location='#/tab/dash';
    };
});
