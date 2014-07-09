module.exports = ["$routeProvider", "$locationProvider", ($routeProvider, $locationProvider) ->
    $routeProvider
        .when "/game/join/:id",
            templateUrl: "/app/code/game/join/join.html"
            controller: "JoinGameCtrl"
            title: "Join Game"

    return
]