module.exports = ["$routeProvider", "$locationProvider", ($routeProvider, $locationProvider) ->
    $routeProvider
        .when "/game/:id/:secret",
            templateUrl: "/app/code/game/ui/ui.html"
            controller: "UICtrl"
            title: "Game"

    return
]