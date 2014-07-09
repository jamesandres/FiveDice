module.exports = ["$routeProvider", "$locationProvider", ($routeProvider, $locationProvider) ->
    $routeProvider
        .when "/game/new",
            templateUrl: "/app/code/game/new/new.html"
            controller: "NewGameCtrl"
            title: "New Game"

    return
]