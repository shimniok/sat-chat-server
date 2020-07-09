(function () {
    'use strict';

    angular.module('RockBlockApp', [])

    .controller('RockBlockController', ['$scope', '$log', '$http', '$timeout',

        function($scope, $log, $http, $timeout) {
            $scope.sendMessage = function() {
                $log.log("sendMessage()");

                // get the URL from the input
                var message = $scope.message;

                // fire the API request
                $http.post('/api/send', {"message": message}).
                    success(function(results) {
                        $log.log(results);
                        return True;
                    }).
                    error(function(error) {
                        $log.log(error);
                        return False;
                    });
            };

            var timeout = "";

            var poller = function() {
                $http.get('/api/message').
                    success(function(data, status, headers, config) {
                        $log.log("poller()");
                        timeout = $timeout(poller, 10000);
                    });
            };
            poller();

        }
    ]);

}());
