module.exports = ["$scope", "$location", "gameAPI", ($scope, $location, gameAPI) ->
    # Fetch games and update the scope
    $scope.games = []
    gameAPI.lobby().then (response) -> $scope.games = response.data.games

    $scope.joinGame = (game) -> $location.path("/game/join/#{game.id}")

    return
]
