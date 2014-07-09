home = angular.module "FD.home", []

home.controller("HomeCtrl", require './HomeCtrl')

home.config(require('./routes'))

module.exports = home
