angular.module('device', ['ngResource'])

.controller('DeviceController', ['$scope', '$log', 'DeviceService',
  function($scope, $log, DeviceService) {
    $scope.myDevice = {};

    $log.log('device controller');

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

  }]);
