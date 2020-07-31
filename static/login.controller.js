angular.module('login', ['session'])

// TODO: fix logout button!

.controller('LoginController', [ '$scope', '$log', '$location', '$http', 'SessionService',
  function($scope, $log, $location, $http, session) {

    $scope.authenticate = function() {
      $log.log("authenticate()");

      session.authenticate($scope.email, $scope.password,
        success = function(result) {
          $log.log("success");
          $location.path("/");
        },
        failure = function() {
          $log.log("failure");
          //TODO: Alert user, clear form
        });
    };

  }
]);
