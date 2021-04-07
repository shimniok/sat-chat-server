(function () {
  "use strict";

  angular
    .module("RockBlockApp", [
      "ngRoute",
      "login",
      "chat",
      "device",
      "message",
      "user",
      "nav",
    ])

    .config(function ($interpolateProvider) {
      $interpolateProvider.startSymbol("//");
      $interpolateProvider.endSymbol("//");
    })

    .config([
      "$routeProvider",
      function ($routeProvider) {
        $routeProvider
          .when("/chat", {
            templateUrl: "static/chat.template.html",
            controller: "ChatController",
            requireAuth: true,
          })
          .when("/device", {
            templateUrl: "static/device.template.html",
            controller: "DeviceController",
            requireAuth: true,
          })
          .when("/login", {
            templateUrl: "static/login.template.html",
            controller: "LoginController",
          })
          .when("/messages", {
            templateUrl: "static/message.template.html",
            controller: "MessageController",
            requireAuth: true,
          })
          .when("/users", {
            templateUrl: "static/user.template.html",
            controller: "UserController",
            requireAuth: true,
          })
          .otherwise({
            redirectTo: "/chat",
          });
      },
    ]);
})();
