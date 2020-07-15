angular.module('session', ['auth'])

.service('SessionService', [ '$log', 'AuthProvider',
function($log, auth) {
  var user = auth.get();

  this.valid = function() {
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
