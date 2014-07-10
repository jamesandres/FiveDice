module.exports = ["$scope", "$location", "$routeParams", "gameAPI", ($scope, $location, $routeParams, gameAPI) ->
    $scope.id = $routeParams.id

    $scope.nick = ""

    $scope.submit = (isValid, id) ->
        if isValid
            gameAPI.join(id, $scope.nick).then (response) ->
                $location.path("/game/#{id}/#{response.data.player.secret}")

    return
]
