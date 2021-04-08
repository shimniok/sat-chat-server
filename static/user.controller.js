angular
  .module("user", ["user.service"])

  .controller("UserController", [
    "$scope",
    "$log",
    "UserService",
    function ($scope, $log, userService) {
      $scope.users = userService.query();
      $scope.newUser = {
        name: "",
        email: "",
        password: "",
      };

      //   $scope.deleteMessage = function(m) {
      //     $log.log("deleteMessage() " + m.id);
      //     userService.delete(m).$promise
      //     .then(function() {
      //       var index = $scope.messages.indexOf(m);
      //       $scope.messages.splice(index, 1);
      //     });
      //   };
    },
  ]);
