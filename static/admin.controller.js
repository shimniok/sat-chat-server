angular.module('admin', ['message'])

.controller('AdminController', ['$scope', '$log', 'MessageService',
function($scope, $log, message) {

  $scope.messages = message.query();

  $scope.deleteMessage = function(m) {
    $log.log("deleteMessage() " + m.id);
    m.$delete().then(function() {
      var index = $scope.messages.indexOf(m);
      $scope.messages.splice(index, 1);
    });
  };

}
]);
