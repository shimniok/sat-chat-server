angular.module('session')

.service('SessionService', [ '$log', 'AuthProvider',
function($log, auth) {
  var isValid = 0;

  this.valid = function() {
    return isValid;
  };

  this.query = function(successCallback, failureCallback) {
    auth.get().$promise
    .then(function(result) {
      isValid = 1;
      successCallback(result);
    }, function(result) {
      isValid = 0;
      failureCallback(result);
    });
  };

  this.authenticate = function(username, password, successCallback, failureCallback) {
    auth.save({ "email": username, "password": password }).$promise
    .then(function(result) {
      isValid = 1;
      successCallback(result);
    },function(result) {
      isValid = 0;
      failureCallback(result);
    });
  }

  this.logout = function() {
    $log.log("SessionService: logout");
    auth.delete();
    isValid = 0;
  }

}]);
