require 'angular/angular'
require 'angular-route/angular-route'


app = angular.module 'FD', [
    'ngRoute',
    require('./home').name,
    require('./lobby').name,
    require('./game').name,
]

# Default route provider
app.config ["$routeProvider", "$locationProvider", ($routeProvider, $locationProvider) ->
    $routeProvider
        .otherwise
            redirectTo: '/home'

    return
]

window.app = app