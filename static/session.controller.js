angular.module('session', ['auth'])

.controller('SessionController', [ '$scope', '$log', '$location', 'SessionService',
  function ($scope, $log, $location, session) {
    $scope.$on('$routeChangeStart', function (angularEvent, next, current) {
      if (next.requireAuth) {
        session.valid().then(
          function() {
            $log.log("session valid");
          },
          function() {
            // TODO: redirect to next after login
            // TODO: the path really should come from somewhere else
            $location.path("/login");
          }
        )
      }
    });
  }
]);
