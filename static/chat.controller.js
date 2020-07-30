angular.module('chat', [
  'rockblock',
  'message'
])

.controller('ChatController', [
  '$scope', '$log', '$timeout', '$location', '$anchorScroll', '$timeout', 'MessageService',
  'MessageSinceService', 'RockBlockProvider',

function($scope, $log, $timeout, $location, $anchorScroll, $timeout, Message, MessageSince, RockBlock) {
  $scope.messages = null;

  var arrayLast = function(a) {
    return a[a.length - 1];
  }

  $log.log($scope.messages);

  //TDOO: Nav Controller, Nav Template

  $scope.admin = function() {
    $location.url("/admin");
  };

  $scope.device = function() {
    $location.url("/device");
  }

  $scope.sendMessage = function() {
    var message = $scope.message;

    if (message)
      RockBlock.send({"message": message}, function(results) {
        $scope.message = ""; // clear form
        getMessages();
      });
  };

  var gotoBottom = function() {
    $timeout(function() {
      $anchorScroll('bottom');
    });
  };

  var getMessages = function() {
    if ($scope.messages == null) {
      $scope.messages = Message.query(function(results) {
        gotoBottom();
      });
    } else {
      last = arrayLast($scope.messages);
      MessageSince.query( {"momsn": last.momsn}, function(results) {
        gotoBottom();
        results.forEach(function(m) {
          $scope.messages.push(m);
        });
      });
    }
  };

  // TODO: backoff algorithm or login timeout

  var timeout = "";

  var poller = function() {
    $log.log("poller()");
    getMessages();
    $scope.timeout = $timeout(poller, 10000);
  };

  poller();

}
]);
