# Goals

Goals for the FiveDice experiment.


## Core goals

- To make use of:
    - Gulp
    - Browserify
    - Karma
    - Backbone
- Taking mobile considerations into account. For example:
    - On 3G / edge, network throughput may be very low and latency very high.
      Great mobile developers take this into account on every interaction.
    - Be responsive. Few things are more frustrating than a laggy app.
    - Related, Handling 300ms tap/click delay
    - Less screen space to work with, compact UI
    - Finger sized controls
    - Controls that give good feedback to taps and gestures
    - Typing on mobile is a PITA. Choosing (by tap) from a few options is
      generally much easier.
    - Generally lower (and different) performance capabilities
    - Designing for HiDpi. Use 'px' measurements if you want a bad time :-P
    - Making use of gestures (sensibly)
    - Tapping fingers cover the tap target. Sometimes this matters for UX..
- Hopefully, a functional app usable on mobile phones where a player can:
    - See the lobby with available games to join
    - Can join an existing game
    - Can, create a game
    - Will wait for others to join before allowing to start making turns
    - Can play with others, see their gambles, etc.
    - If player lost, can continue to observe the game until its conclusion
    - Can quit a game at any time
    - Can watch other games in progress
- Has a handful of real unit tests


## Stretch goals (in any order)

- Support for i18n via Jed.js or similar.
- Experiment with alternate libraries and frameworks
    - Backbone Marionette
    - A mobile UI CSS framework, eg: Bootstrap 3.
    - Knockout.js
    - Handlebars.js
- Support for l10n, check out https://docs.angularjs.org/guide/i18n for
  inspiration
- In depth unit testing for the app
- Invent another goal!
