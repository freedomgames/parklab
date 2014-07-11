var planet_app = angular.module('planet_app', ['ngRoute']);

planet_app.config(['$controllerProvider', '$provide', '$compileProvider', '$routeProvider', function($controllerProvider, $provide, $compileProvider, $routeProvider){
    /* CODE FOR ASYNC MODULE LOADING */
    planet_app._controller = planet_app.controller;
    planet_app._service = planet_app.service;
    planet_app._factory = planet_app.factory;
    planet_app._directive = planet_app.directive;

    planet_app.controller = function( name, constructor ) {
        $controllerProvider.register( name, constructor );
        return( this );
    };

    planet_app.service = function( name, constructor ) {
        $provide.service( name, constructor );
        return( this );
    };

    planet_app.factory = function( name, factory ) {
        $provide.factory( name, factory );
        return( this );
    };

    planet_app.directive = function( name, factory ) {
        $compileProvider.directive( name, factory );
        return( this );
    };

    $routeProvider
        // route for the home page
        .when('/', {
                templateUrl: 'homepage/homepage.html',
                resolve: {
                    deps: function($q, $rootScope) {
                        var deferred = $q.defer();
                        var dependencies = [
                            'homepage/homepagectrl.js'
                        ];

                        $script(dependencies, function(){
                            $rootScope.$apply(function(){
                                deferred.resolve();
                            });
                        });

                        return deferred.promise;
                    }
                },
                controller: 'HomepageCtrl'
            })
        .when('/mentors', {
            templateUrl: 'users/mentors.html',
            resolve: {
                    deps: function($q, $rootScope) {
                        var deferred = $q.defer();
                        var dependencies = [
                            'users/mentorsctrl.js'
                        ];

                        $script(dependencies, function(){
                            $rootScope.$apply(function(){
                                deferred.resolve();
                            });
                        });

                        return deferred.promise;
                    }
                },
            controller: 'MentorsCtrl'
        })
        .when('/profile', {
            templateUrl: 'profile/profile.html',
            resolve: {
                    deps: function($q, $rootScope) {
                        var deferred = $q.defer();
                        var dependencies = [
                            'profile/profilectrl.js'
                        ];

                        $script(dependencies, function(){
                            $rootScope.$apply(function(){
                                deferred.resolve();
                            });
                        });

                        return deferred.promise;
                    }
                },
            controller: 'ProfileCtrl'
        })
        .when('/organization', {
            templateUrl: 'organization/organization.html',
            resolve: {
                    deps: function($q, $rootScope) {
                        var deferred = $q.defer();
                        var dependencies = [
                            'organization/organizationctrl.js'
                        ];

                        $script(dependencies, function(){
                            $rootScope.$apply(function(){
                                deferred.resolve();
                            });
                        });

                        return deferred.promise;
                    }
                },
            controller: 'OrganizationCtrl'
        })
        .when('/assembly',{
            templateUrl: 'assembly/assembly.html',
            resolve: {
                    deps: function($q, $rootScope) {
                        var deferred = $q.defer();
                        var dependencies = [
                            'assembly/assemblyctrl.js'
                        ];

                        $script(dependencies, function(){
                            $rootScope.$apply(function(){
                                deferred.resolve();
                            });
                        });

                        return deferred.promise;
                    }
                },
            controller: 'AssemblyCtrl'
        })
        .otherwise({ redirectTo: '/' });
}]);

planet_app.run(function($rootScope, $location){
    $rootScope.pageLocation = window.location.href.substr(window.location.href.lastIndexOf('/') + 1);
    $rootScope.$on('$routeChangeSuccess', function(event) {
        $rootScope.pageLocation = window.location.href.substr(window.location.href.lastIndexOf('/') + 1);
    });
});