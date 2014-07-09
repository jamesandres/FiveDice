newGame = angular.module "FD.game.new", []

newGame.controller("NewGameCtrl", require './NewGameCtrl')

newGame.config(require('./routes'))

module.exports = newGame
