module.exports = ->
    return {
        restrict: "E",
        templateUrl: "/app/code/game/ui/PlayersList.html",
        scope: {
            players: '='
        }
    }
