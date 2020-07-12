(function () {
    'use strict';

    angular.module('app', ['message', 'rockblock'])

    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
    })

    .controller('RockBlockController', ['$scope', '$log', '$timeout', 'Message', 'MessageSince', 'RockBlock',

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


            $scope.deleteMessage = function(message) {
                $log.log("deleteMessage()");
                Message.delete(message, function() {
                    var index = $scope.messages.indexOf(message);
                    $scope.messages.splice(index, 1);
                });
            };


            var getNewMessages = function() {
                MessageSince.query(arrayLast($scope.messages), function(results) {
                    results.forEach(function(m) {
                        $scope.messages.push(m);
                    });
                });
            }

            var timeout = "";

            var poller = function() {
                $log.log("poller()");
                getNewMessages();
                $scope.timeout = $timeout(poller, 10000);
            };

            poller();

        }
    ]);

}());
