(function () {
    'use strict';

    angular.module('RockBlockApp', [])

    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
    })

    .controller('RockBlockController', ['$scope', '$log', '$http', '$timeout',

        function($scope, $log, $http, $timeout) {
            var current_user = $scope.current_user;
            var last_momsn = -1;

            $scope.messages = [];

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
                $http.delete('/api/message/' + message.id).then(
                    function (response) {
                        var index = $scope.messages.indexOf(message);
                        $scope.messages.splice(index, 1);
                    });
            };

            var updateLast = function() {
                last_momsn = $scope.messages[$scope.messages.length - 1].momsn;
            }

            var getMessages = function() {
                $log.log("getMessages()");
                $http.get('/api/message')
                    .success(function(results, status, headers, config) {
                        $log.log(results);
                        $scope.messages = results;
                        updateLast();
                        $log.log("last_momsn =",last_momsn);
                    });
            }

            var getNewMessages = function() {
                $http.get('/api/message/since/'+last_momsn)
                    .success(function(results, status, headers, config) {
                        $log.log("since length: " + results.length);
                        if (results.length > 0) {
                            $log.log(results);
                            results.forEach(function(m) {
                                $scope.messages.push(m);
                            });
                            updateLast();
                        }
                    });
            }

            var timeout = "";

            var poller = function() {
                $log.log("poller()");
                getNewMessages();
                $scope.timeout = $timeout(poller, 30000);
            };

            getNewMessages();
            poller();

        }
    ]);

}());
