module.exports = ["$routeProvider", "$locationProvider", ($routeProvider, $locationProvider) ->
    $routeProvider
        .when "/home",
            templateUrl: "/app/code/home/home.html"
            controller: "HomeCtrl"
            title: "Home"

    return
]