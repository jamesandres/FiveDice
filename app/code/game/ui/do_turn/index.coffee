doTurn = angular.module "FD.game.ui.do_turn", []

doTurn.directive("doTurnForm", require './DoTurnForm')

module.exports = doTurn
