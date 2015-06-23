angular.module('starter.controllers', [])


.controller('PlacesCtrl', function($scope, Places) {
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //
  //$scope.$on('$ionicView.enter', function(e) {
  //});

 Places.all(function(data, status) {
       $scope.Places=data;
 });

})

.controller('AccountCtrl', function($scope) {

});
