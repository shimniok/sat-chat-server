angular.module('login', ['auth'])

.service('SessionService', [ '$log', 'AuthProvider',
function($log, auth) {
  var user = auth.get();

  this.check = function() {
    return user.$promise;
  };

  this.login = function(username, password, success, failure) {
    auth.save({ "email": username, "password": password }).$promise
    .then(function(result) {
      user = result;
      success(result);
    },function(result) {
      failure(result);
    });
  }

  this.logout = function() {
    user = auth.delete();
  }

}])

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
