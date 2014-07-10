module.exports = ["$scope", "$location", "gameAPI", ($scope, $location, gameAPI) ->
    $scope.nick = ""
    $scope.numPlayers = 2

    $scope.submit = (isValid, id) ->
        if isValid
            gameAPI.new($scope.nick, $scope.numPlayers).then (response) ->
                data = response.data
                $location.path("/game/#{data.game.id}/#{data.player.secret}")

    return
]
