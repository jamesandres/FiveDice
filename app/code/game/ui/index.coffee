ui = angular.module "FD.game.ui", [
    require('./do_turn').name,
]

ui.controller("UICtrl", require './UICtrl')

ui.directive("playersList", require './PlayersList')
ui.directive("gameRound", require './GameRound')
ui.directive("dice", require './Dice')

ui.config(require('./routes'))

module.exports = ui
