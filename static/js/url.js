angular.module('hornbook', []).
    config(['$routeProvider', function($routeProvider) {
    $routeProvider.
        when('/api', {
            templateUrl: 'templates/hornbook_api/index.html', 
            controller: HornbookAPICtrl
        })
}]);