angular.module('session', ['auth'])

.controller('SessionController', [ '$scope', '$log', '$location', 'SessionService',
  function ($scope, $log, $location, session) {

    $scope.user = session.getUser();

    // Intercept route changes and check if authentication is required and if so, check session validity
    $scope.$on('$routeChangeStart', function (angularEvent, next, current) {
      if (next.requireAuth) {
        session.valid().then(
          function() {
            $log.log("session valid");
          },
          function() {
            // TODO: redirect to next after login
            // TODO: the path really should come from somewhere else
            $log.log("session invalid");
            $location.path("/login");
          }
        )
      }
    });
  }
]);
