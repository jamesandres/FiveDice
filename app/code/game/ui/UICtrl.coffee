module.exports = ["$scope", "$location", "$routeParams", ($scope, $location, $routeParams) ->
    $scope.id = $routeParams.id
    $scope.secret = $routeParams.secret


    return
]
