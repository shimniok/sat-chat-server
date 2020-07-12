angular.module('message', ['ngResource']);

angular.module('message')
    .factory('Message', ['$resource',
        function($resource) {
            return $resource('/api/message/:id');
        }
  ]);
