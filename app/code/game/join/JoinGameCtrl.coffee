module.exports = ["$scope", "$location", "$routeParams", "gameAPI", ($scope, $location, $routeParams, gameAPI) ->
    $scope.id = $routeParams.id
    $scope.nick = ""
    $scope.lastError = ""

    $scope.submit = (isValid, id) ->
        if isValid
            gameAPI.join(id, $scope.nick).then (response) ->
                data = response.data
                if data.error
                    $scope.lastError = data.error
                else
                    $location.path("/game/#{id}/#{response.data.player.secret}")

    return
]
