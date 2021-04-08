angular
  .module("chat", ["rockblock.service", "message.service"])

  .controller("ChatController", [
    "$scope",
    "$log",
    "$timeout",
    "$anchorScroll",
    "MessageService",
    "MessageSinceService",
    "RockBlockProvider",
    "SessionService",

    function (
      $scope,
      $log,
      $timeout,
      $anchorScroll,
      messageService,
      messageSinceService,
      rockBlockService,
      session
    ) {
      $scope.messages = messageService.query();

      var arrayLast = function (a) {
        return a == null || a.length == 0 ? null : a[a.length - 1];
      };

      $log.log($scope.messages);

      $scope.sendMessage = function () {
        var message = $scope.message;

        if (message)
          rockBlockService.send({ message: message }, function (results) {
            $scope.message = ""; // clear form
            getMessages();
          });
      };

      var gotoBottom = function () {
        $timeout(function () {
          $anchorScroll("bottom");
        });
      };

      var getMessages = function () {
        if ($scope.messages == null) {
          $scope.messages = messageService.query(function () {
            gotoBottom();
          });
        } else {
          last = arrayLast($scope.messages);
          if (last != null) {
            messageSinceService.query(
              { momsn: last.momsn },
              function (results) {
                gotoBottom();
                results.forEach(function (m) {
                  $scope.messages.push(m);
                });
              }
            );
          }
        }
      };

      // TODO: backoff algorithm or login timeout

      var timeout = "";

      var poller = function () {
        $log.log("poller()");
        if (session.valid()) {
          getMessages();
        }
        $scope.timeout = $timeout(poller, 30000);
      };

      poller();
    },
  ]);
