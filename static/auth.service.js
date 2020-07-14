angular.module('auth', [])

.factory('AuthProvider', ['$resource',
    function($resource) {
        return $resource('/auth');
    }
]);
