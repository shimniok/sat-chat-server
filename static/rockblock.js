angular.module('rockblock', ['ngResource'])
    .factory('RockBlock', ['$resource',
        function($resource) {
            return $resource('/api/send', {}, {
                'send': { method: 'post' }
            });
        }
    ]);
