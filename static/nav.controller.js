angular.module('nav', [])

.controller('NavController', ['$scope', '$location', '$log', 
function($scope, $location, $log) {

    $scope.chat = function() {
        $log.log("nav to chat");
        $location.url("/chat");
    }

    $scope.device = function () {
        $log.log("nav to device");
        $location.url("/device");
    };

    $scope.messages = function () {
        $log.log("nav to messages");
        $location.url("/messages");
    };

    $scope.users = function () {
        $log.log("nav to users");
        $location.url("/users");
    };

}])

.directive('navBar', function() {
    return {
        restrict: 'E',
        templateUrl: 'static/nav.template.html'
    };
});
