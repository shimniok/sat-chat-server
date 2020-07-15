angular.module('login', ['session'])

.controller('SessionController', [ '$scope', '$log', '$location', 'SessionService',
  function ($scope, $log, $location, session) {
    $scope.$on('$routeChangeStart', function (angularEvent, next, current) {
      if (next.requireAuth) {
        session.valid().then(
          function() {
            $log.log("session valid");
          },
          function() {
            $location.path("/login"); // TODO: redirect to next after login
          }
        )
      }
    });
  }
])


.controller('LoginController', [ '$scope', '$log', '$location', '$http', 'SessionService', 'AuthProvider',
  function($scope, $log, $location, $http, session, auth) {

    $scope.logout = function() {
      $log.log("logout()");
      session.logout();
      $location.path("/");
    }

    $scope.authenticate = function() {
      $log.log("authenticate()");

      session.login($scope.email, $scope.password,
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
