angular.module('chat', [
  'rockblock',
  'message'
])

.controller('ChatController', [
  '$scope', '$log', '$timeout', 'MessageService', 'MessageSinceService', 'RockBlockProvider', 'SessionService',

function($scope, $log, $timeout, Message, MessageSince, RockBlock, session) {
  $scope.messages = Message.query();
  $scope.user = session.getUser();

  var arrayLast = function(a) {
    return a[a.length - 1];
  }

  $log.log($scope.messages);

  $scope.sendMessage = function() {
    var message = $scope.message;

    if (message)
    RockBlock.send({"message": message}, function(results) {
      $log.log(results);
      $scope.messages.push(results.message);
      $scope.message = ""; // clear form
    });
  };

  var getNewMessages = function() {
    MessageSince.query(arrayLast($scope.messages), function(results) {
      results.forEach(function(m) {
        $scope.messages.push(m);
      });
    });
  }

  // TODO: backoff algorithm or login timeout

  var timeout = "";

  var poller = function() {
    $log.log("poller()");
    getNewMessages();
    $scope.timeout = $timeout(poller, 60000);
  };

  poller();

}
]);
