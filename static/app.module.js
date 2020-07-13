(function () {
  'use strict';

  angular.module('RockBlockApp', [
    'ngRoute',
    'message',
    'login',
    'chat.controller'
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
