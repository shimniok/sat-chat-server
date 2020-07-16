(function () {
  'use strict';

  angular.module('RockBlockApp', [
    'ngRoute',
    'login',
    'chat',
    'admin',
    'chat.device'
  ])

  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('//');
    $interpolateProvider.endSymbol('//');
  })

  .config(['$routeProvider', function($routeProvider) {
    $routeProvider
    .when('/chat', {
      templateUrl: 'static/chat.template.html',
      controller: 'ChatController',
      requireAuth: true
    })
    .when('/login', {
      templateUrl: 'static/login.template.html',
      controller: 'LoginController'
    })
    .when('/admin', {
      templateUrl: 'static/admin.template.html',
      controller: 'AdminController'
    })
    .when('/device', {
      templateUrl: 'static/device.template.html',
      controller: 'DeviceController'
    })
    .otherwise({
      redirectTo: '/chat'
    })
  }]);

}());
