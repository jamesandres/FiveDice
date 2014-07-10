module.exports = ["$http", ($http) ->
    return {
        # All of these services return XHR promises for their results. Gather
        # the data by binding a .then(), .error() or .done() method.
        lobby: -> $http.get "/game/lobby"
        # FIXME: Currently fails because the backend does not accept JSON POST
        new: (nick) -> $http.post "/game/new", {"nick": nick}
        # FIXME: Currently fails because the backend does not accept JSON POST
        join: (id, nick) -> $http.post "/game/#{id}/join", {"nick": nick}
    }
]
