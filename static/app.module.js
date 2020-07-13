(function () {
  'use strict';

  angular.module('RockBlockApp', [
    'ngRoute',
    'login',
    'chat'
  ])

  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('//');
    $interpolateProvider.endSymbol('//');
  })

  .config(['$routeProvider', function($routeProvider) {
    $routeProvider
    .when('/chat', {
      templateUrl: 'static/chat.template.html',
      controller: 'ChatController'
    })
    .when('/login', {
      templateUrl: 'static/login.template.html',
      controller: 'LoginController'
    })
    /*
    .when('/chat/admin', {
      templateUrl: 'admin.html',
      controller: 'AdminController'
    })
    */
    .otherwise({
      redirectTo: '/chat'
    })
  }]);

}());
