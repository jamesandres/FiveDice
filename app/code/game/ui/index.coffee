ui = angular.module "FD.game.ui", []

ui.controller("UICtrl", require './UICtrl')

ui.config(require('./routes'))

module.exports = ui
