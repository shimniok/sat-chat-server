(function () {
    'use strict';

    angular.module('app', ['message'])

    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
    })

    .controller('RockBlockController', ['$scope', '$log', '$http', '$timeout', 'Message', 'MessageSince',

        function($scope, $log, $http, $timeout, Message, MessageSince) {
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
                $log.log("sendMessage()");

                // get the URL from the input
                var message = $scope.message;

                // fire the API request
                $http.post('/api/send', {"message": message})
                    .success(function(results, status, headers, config) {
                        $log.log(results);
                        getNewMessages();
                        $scope.message = ""; // clear form
                    }).
                    error(function(error) {
                        $log.log(error);
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
