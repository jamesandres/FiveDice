module.exports = ["$scope", "$location", "$routeParams", "gameAPI", ($scope, $location, $routeParams, gameAPI) ->
    $scope.id = $routeParams.id
    $scope.secret = $routeParams.secret

    $scope.lastError = ""

    $scope.game = {}
    $scope.player = {}

    gameAPI.state($scope.id, $scope.secret).then (response) ->
        data = response.data

        if data.error
            $scope.lastError = data.error
        else
            $scope.game = data.game
            $scope.player = data.player

            dice = data.player.dice
            if dice
                $scope.dice = (parseInt(d, 10) for d in dice.split(','))
            else
                $scope.dice = []

    return
]
