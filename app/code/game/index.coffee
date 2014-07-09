game = angular.module "FD.game", [
    require('./new').name,
    require('./join').name,
    require('./ui').name,
]

game.factory("gameAPI", require('./gameAPI'))

module.exports = game