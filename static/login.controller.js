angular.module('login', [])

.service('SessionService', function() {
  var user = null;

  this.isAuthenticated = function(value){
    return user != null;
  };

})

.controller('LoginController', [ '$scope', '$log', '$http',
  function($scope, $log, $http) {

    $scope.authenticate = function() {
      $log.log("authenticate()");

      var data = {
        "email": $scope.email,
        "password": $scope.password
      };
      var config = { headers: { 'Content-Type': 'application/json', 'Accepts': 'application/json' } }
      $http.post('/auth', data, config)
        .success(function(result) {
          $log.log("success");
          this.user = result;
        },
        function() {
          $log.log("failure");
        });
      };

  }
]);
