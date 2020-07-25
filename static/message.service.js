angular.module('message', ['ngResource'])
    .factory('MessageService', ['$resource',
        function($resource) {
            return $resource('/api/message/:id', {});
        }
    ])
    .factory('MessageSinceService', ['$resource',
        function($resource) {
            return $resource('/api/message/since/:momsn');
        }
    ]);
