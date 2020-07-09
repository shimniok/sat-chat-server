(function () {
    'use strict';

    angular.module('RockBlockApp', [])

    .controller('RockBlockController', ['$scope', '$log', '$http',
        function($scope, $log, $http) {
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
        }
    ]);

}());
