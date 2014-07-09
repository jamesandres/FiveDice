joinGame = angular.module "FD.game.join", []

joinGame.controller("JoinGameCtrl", require './JoinGameCtrl')

joinGame.config(require('./routes'))

module.exports = joinGame
