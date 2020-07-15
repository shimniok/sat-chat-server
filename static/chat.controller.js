angular.module('chat', [
  'rockblock',
  'message'
])

.controller('ChatController', [
  '$scope', '$log', '$timeout', 'MessageService', 'MessageSinceService', 'RockBlockProvider',

function($scope, $log, $timeout, Message, MessageSince, RockBlock) {
  var current_user = $scope.current_user;

  $scope.messages = Message.query();

  var arrayLast = function(a) {
    return a[a.length - 1];
  }

  $log.log($scope.messages);

  $scope.matchUser = function(user) {
    return (user == current_user);
  };

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
    $scope.timeout = $timeout(poller, 10000);
  };

  poller();

}
]);
