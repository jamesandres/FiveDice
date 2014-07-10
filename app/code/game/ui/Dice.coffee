module.exports = ->
    return {
        restrict: "E",
        template: '''
            <ul class="dice">
                <li ng-repeat="die in dice track by $index"
                    class="die die-{{die}}">{{die}}</li>
            </ul>
        ''',
        scope: {
            dice: '='
        }
    }
