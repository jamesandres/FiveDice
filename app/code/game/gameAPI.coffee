module.exports = ["$http", ($http) ->
    return {
        # All of these services return XHR promises for their results. Gather
        # the data by binding a .then(), .error() or .done() method.
        lobby: -> $http.get "/game/lobby"

        new: (nick, num_players) ->
            $http.post "/game/new",
                "nick": nick
                "num_players": num_players

        join: (id, nick) ->
            $http.post "/game/#{id}/join",
                "nick": nick

        publicState: (id) -> $http.get "/game/#{id}"

        state: (id, secret) -> $http.get "/game/#{id}/#{secret}"
    }
]
