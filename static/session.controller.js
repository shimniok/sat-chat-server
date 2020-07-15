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
            $location.path("/login"); // TODO: redirect to next after login
          }
        )
      }
    });
  }
]);
