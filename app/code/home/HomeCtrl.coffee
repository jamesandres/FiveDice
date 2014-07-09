module.exports = ["$scope", "$location", ($scope, $location) ->
    $scope.goToLobby   = -> $location.path('lobby')
    $scope.goToNewGame = -> $location.path('game/new')

    return
]
