angular
  .module("device.service", ["ngResource"])

  .factory("DeviceService", [
    "$resource",
    function ($resource) {
      return $resource("/api/device/:id", { id: "@id" });
    },
  ]);
