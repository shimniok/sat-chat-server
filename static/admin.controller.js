angular.module('admin', ['message'])

.controller('AdminController', ['$scope', '$log', 'MessageService',
function($scope, $log, messageService) {

  $scope.messages = messageService.query();

  $scope.deleteMessage = function(m) {
    $log.log("deleteMessage() " + m.id);
    messageService.delete(m).$promise
    .then(function() {
      var index = $scope.messages.indexOf(m);
      $scope.messages.splice(index, 1);
    });
  };

}
]);
