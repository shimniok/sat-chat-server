angular.module('rockblock', ['ngResource'])
.factory('RockBlockProvider', ['$resource',
  function($resource) {
    return $resource('/api/send', {}, {
      'send': { method: 'post' }
    });
  }
]);
