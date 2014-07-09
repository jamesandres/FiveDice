lobby = angular.module "FD.lobby", []

lobby.controller("LobbyCtrl", require './LobbyCtrl')

lobby.config(require('./routes'))

module.exports = lobby
