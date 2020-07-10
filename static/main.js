(function () {
    'use strict';

    angular.module('RockBlockApp', [])

    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
    })

    .controller('RockBlockController', ['$scope', '$log', '$http', '$timeout',

        function($scope, $log, $http, $timeout) {

            var messages = [];
            var test="test";
            var current_user = $scope.current_user;

            $scope.matchUser = function(user) {
                return (user == current_user) ? 'level-right' : 'level-left';
            };

            $scope.sendMessage = function() {
                $log.log("sendMessage()");

                // get the URL from the input
                var message = $scope.message;

                // fire the API request
                $http.post('/api/send', {"message": message}).
                    success(function(results) {
                        $log.log(results);
                    }).
                    error(function(error) {
                        $log.log(error);
                    });
            };

            var timeout = "";

            var poller = function() {
                $http.get('/api/message').
                    success(function(data, status, headers, config) {
                        $log.log("poller()");
                        $scope.messages = data;
                        $scope.timeout = $timeout(poller, 10000);
                    });
            };
            poller();

        }
    ]);

}());
