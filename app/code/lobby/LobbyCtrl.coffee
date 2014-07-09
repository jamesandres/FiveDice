module.exports = ["$scope", "$location", ($scope, $location) ->
    $scope.games = [
        {
            "id": 1,
            "players": [
                {
                    "nick": "James"
                },
                {
                    "nick": "Elaine"
                }
            ],
            "player_nicks": ["James", "Elaine"]
        }
    ]

    return
]
