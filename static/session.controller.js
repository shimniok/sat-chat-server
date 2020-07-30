angular.module('session', ['auth'])

.controller('SessionController', [ '$scope', '$log', '$location', 'SessionService',
  function ($scope, $log, $location, session) {

    $scope.user = session.getUser();

    // Intercept route changes and check if authentication is required
    // and if so, check session validity
    $scope.$on('$routeChangeStart', function (angularEvent, next, current) {
      $log.log("routeChangeStart");
      if (next.requireAuth) {
        session.valid().then(
          function() {
            $log.log("SessionController: session valid");
          },
          function() {
            // TODO: redirect to next after login
            // TODO: the path really should come from somewhere else
            $log.log("SessionController: session invalid");
            $location.path("/login");
          }
        )
      }
    });

    $scope.logout = function() {
      $log.log("SessionController: logging out");
      session.logout();
      $location.path("/login");
    }

  }
]);
