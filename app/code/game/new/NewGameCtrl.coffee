module.exports = ["$scope", "$location", ($scope, $location) ->
    $scope.nick = ""
    $scope.numPlayers = 2

    $scope.submit = (isValid, id) ->
        if isValid
            gameAPI.new($scope.nick).then (response) ->
                data = response.data
                $location.path("/game/#{data.game.id}/#{data.player.secret}")

    return
]
