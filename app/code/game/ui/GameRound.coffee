module.exports = ->
    return {
        restrict: "E",
        template: '''
            <h2 class="game-round">
                <span class="round-name">Round</span>
                <span class="round-number">{{round}}</span>
            </h2>
        ''',
        scope: {
            round: '='
        }
    }
