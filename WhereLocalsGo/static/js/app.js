// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'starter.services' is found in services.js
// 'starter.controllers' is found in controllers.js
angular.module('starter', ['ionic', 'starter.controllers', 'starter.services'])

.run(function($rootScope,$ionicPlatform,$location) {
  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if (window.cordova && window.cordova.plugins && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
    }
    if (window.StatusBar) {
      // org.apache.cordova.statusbar required
      StatusBar.styleLightContent();
    }
  });
  $rootScope.preferences = {
    time:'',
    weekday:'',
    age: 33,
    gender: '',
    amount:2,
    local:false,
    customerzipcode:''
  };
  $rootScope
      .$on('$stateChangeSuccess',
      function(event){
        if (!window.ga)
          return;
        window.ga('send', 'pageview', { page: $location.path() });
      });

})

.filter('escape', function() {
  return window.encodeURIComponent;
})

.config(function($stateProvider, $urlRouterProvider) {

  // Ionic uses AngularUI Router which uses the concept of states
  // Learn more here: https://github.com/angular-ui/ui-router
  // Set up the various states which the app can be in.
  // Each state's controller can be found in controllers.js
  $stateProvider

  // setup an abstract state for the tabs directive
  .state('tab', {
    url: "/tab",
    abstract: true,
    templateUrl: "/static/views/tabs.html"
  })

  // Each tab has its own nav history stack:



  .state('tab.account', {
    url: '/account',
    views: {
      'tab-account': {
        templateUrl: '/static/views/tab-account.html',
        controller: 'AccountCtrl'
      }
    }
  })
      
  .state('tab.map', {
    cache: false,
    url: '/map',
    views: {
      'tab-map': {
        templateUrl: '/static/views/tab-map.html',
        controller: 'MapCtrl'
      }
    }
  })

  .state('tab.dash', {
    cache: false,
    url: '/dash',
    views: {
      'tab-dash': {
        templateUrl: '/static/views/tab-dash.html',
        controller: 'PlacesCtrl'
      }
    }
  });

  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise('/tab/account');

});
