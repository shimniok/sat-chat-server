angular.module('device', ['ngResource'])

.controller('DeviceController', ['$scope', '$log', 'DeviceService',
  function($scope, $log, DeviceService) {
    $scope.myDevice = {};

    // see if we have a device already and if so, assign to model
    DeviceService.query(content_type='application/json').$promise
    .then(function(result) {
      $log.log(result);
      if (result.length != 0) {
        r = result[0];
        $scope.username = r.username;
        $scope.imei = r.imei;
        $scope.password = "password"; // bogus password
      }
    });

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
