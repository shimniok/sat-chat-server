angular.module('login', ['session'])

// TODO: fix logout button!

.controller('LoginController', [ '$scope', '$log', '$location', '$http', 'SessionService', 'AuthProvider',
  function($scope, $log, $location, $http, session, auth) {

    $scope.logout = function() {
      $log.log("logout()");
      session.logout();
      $location.path("/");
    }

    $scope.authenticate = function() {
      $log.log("authenticate()");

      session.authenticate($scope.email, $scope.password,
        success = function(result) {
          $log.log("success");
          $location.path("/");
        },
        failure = function() {
          $log.log("failure");
        });
    };

  }
]);
