angular.module('login', [])

.service('SessionService', function() {
  var user = null;

  this.authenticated = function() {
    return user != null;
  };

})

.controller('SessionController', [ '$scope', '$log', '$location', 'SessionService',
  function ($scope, $log, $location, session) {
    $scope.$on('$routeChangeStart', function (angularEvent, next, current) {
      if (next.requireAuth && !session.user) {
        $location.path("/login"); // TODO: redirect parameter
      }
    });
  }
])


.controller('LoginController', [ '$scope', '$log', '$location', '$http', 'SessionService',
  function($scope, $log, $location, $http, session) {

    $scope.authenticate = function() {
      $log.log("authenticate()");

      $http.post('/auth', {
        "email": $scope.email,
        "password": $scope.password
      })
      .success(function(result) {
        $log.log("success");
        session.user = result;
        $location.path("/");
      },
      function() {
        $log.log("failure");
      });
    };

  }
]);
