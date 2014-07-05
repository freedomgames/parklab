planet_app.factory('getterFactory', function($http){
    return {
        getItems: function($target, callback) {
            $http({
                url: 'http://jsonstub.com/users/' + $target,
                method: 'GET',
                headers: {
                    'JsonStub-User-Key': '49e06777-c932-4ac8-8068-84f12d0c99ea',
                    'JsonStub-Project-Key': 'b4501f95-faaa-4846-b96b-83bd3b4bdb40'
                }
            }).success(function (data, status, headers, config) {
                callback(data);
            });
        },
        getItem: function($target, callback) {
            $http({
                url: 'http://jsonstub.com/user/' + $target,
                method: 'GET',
                headers: {
                    'JsonStub-User-Key': '49e06777-c932-4ac8-8068-84f12d0c99ea',
                    'JsonStub-Project-Key': 'b4501f95-faaa-4846-b96b-83bd3b4bdb40'
                }
            }).success(function (data, status, headers, config) {
                callback(data);
            });
        }
    }
})