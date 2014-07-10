module.exports = ->
    return {
        restrict: "E",
        template: '''
            <div class="buttons-pane">
                <button>Make a bet!</button>
                <button>Call bullshit</button>
                <button>Call exact</button>
            </div>
        ''',
        controller: require('./DoTurnFormCtrl').name,
        scope: {}
    }
