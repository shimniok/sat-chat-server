angular.module('device', ['ngResource'])

.controller('DeviceController', ['$scope', '$log', 'DeviceService',
  function($scope, $log, DeviceService) {
    $scope.device = null;

    // see if we have a device already and if so, assign to model
    DeviceService.query(content_type='application/json').$promise
    .then(function(result) {
      if (result.length > 0) {
        $log.log(result[0]);
        $scope.device = result[0];
        //$scope.password = "password"; // bogus password as placeholder
        $scope.username = result[0].username;
        $scope.imei = result[0].imei;
      }
      return result[0];
    }, function(result) {
      $scope.device = null;
    });

    $scope.save = function() {
      $log.log('DeviceController: save');

      var newDevice = {
        "imei": $scope.imei,
        "username": $scope.username,
        "password": $scope.password
      }

      DeviceService.save(newDevice, function(result) {
        $log.log('DeviceController: save() success');
        $scope.imei = '';
        $scope.username = '';
        $scope.password = '';
      });

    };

    $scope.update = function() {
      $log.log('DeviceController: update');

      var update = {};

      if ($scope.imei != $scope.device.imei) update.imei = $scope.imei;
      if ($scope.username != $scope.device.username) update.username = $scope.username;

      if ($scope.password1 != "" && $scope.password1 == $scope.password2) {
        update.password = $scope.password1;
      }

    };

  }]);
