module.exports = ["$routeProvider", "$locationProvider", ($routeProvider, $locationProvider) ->
    $routeProvider
        .when "/lobby",
            templateUrl: "/app/code/lobby/lobby.html"
            controller: "LobbyCtrl"
            title: "Lobby"

    return
]