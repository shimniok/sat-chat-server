angular
  .module("device", ["device.service"])

  .controller("DeviceController", [
    "$scope",
    "$log",
    "DeviceService",

    function ($scope, $log, deviceService) {
      // see if we have a device already and if so, assign to model
      getDevice = function () {
        deviceService.query((content_type = "application/json")).$promise.then(
          function (result) {
            if (result.length > 0) {
              $log.log(result[0]);
              $scope.device = result[0];
            }
            return result[0];
          },
          function (result) {
            return {
              imei: "",
              username: "",
              password: "",
            };
          }
        );
      };

      $scope.save = function () {
        $log.log("DeviceController: save");

        // If id property present, then we're updating not saving.
        // if ('id' in $scope.device) {
        // }

        // Only copy password if it's been changed
        if ($scope.password1 != "") $scope.device.password = $scope.password1;

        deviceService.save($scope.device, function (result) {
          $log.log("DeviceController: save() success");
          $scope.device = getDevice();
          $scope.password1 = "";
        });
      };

      $scope.device = getDevice();
    },
  ]);
