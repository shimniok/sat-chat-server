angular.module('session', ['auth'])

.controller('SessionController', [ '$scope', '$log', '$location', 'SessionService',
  function ($scope, $log, $location, session) {

    $scope.user = null;

    // Intercept route changes and check if authentication is required
    // and if so, check session validity
    $scope.$on('$routeChangeStart', function (angularEvent, next, current) {
      $log.log("routeChangeStart");
      if (next.requireAuth) {
        session.query(function(result) {
          $scope.user = result;
        }, function(result) {
          $scope.user = null;
          $log.log("SessionController: session invalid");
          $location.path("/login");
        });
      }
    });

    $scope.logout = function() {
      $log.log("SessionController: logging out");
      session.logout();
      $location.path("/login");
    }

  }
]);
