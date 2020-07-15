angular.module('message', ['ngResource'])
    .factory('MessageService', ['$resource',
        function($resource) {
            return $resource('/api/message/:id', { id: '@id' });
        }
    ])
    .factory('MessageSinceService', ['$resource',
        function($resource) {
            return $resource('/api/message/since/:momsn', {momsn: '@momsn'});
        }
    ]);
