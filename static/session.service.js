angular.module('session')

.service('SessionService', [ '$log', 'AuthProvider',
function($log, auth) {
  var user = auth.get();

  this.getUser = function() {
    return user;
  };

  this.valid = function() {
    user = auth.get();

    return user.$promise;
  };

  this.authenticate = function(username, password, success, failure) {
    auth.save({ "email": username, "password": password }).$promise
    .then(function(result) {
      user = result;
      success(result);
    },function(result) {
      failure(result);
    });
  }

  this.logout = function() {
    $log.log("SessionService: logout");
    user = auth.delete();
  }

}]);
