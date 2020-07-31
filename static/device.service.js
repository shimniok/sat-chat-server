angular.module('device')
.factory('DeviceService', ['$resource',
  function($resource) {
    return $resource('/api/device/:id');
  }
]);
