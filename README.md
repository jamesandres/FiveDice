# FiveDice Game Reenactment

- First player creates a new game and implicitly joins it as the first
  participant. The server sends them their player number and a unique game
  URL with an embedded token that identifies the player for each request
  Security! ;-)

      POST /game/new {"num_players": 3, "nick": "acidburn"}
      ~> {
             "game_url": "http://localhost:8000/game/123/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
             "player": {
                 "nick": "acidburn",
                 "secret": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                 "number": 1
             },
             "game": {
                 "num_players": "3",
                 "status": 1,
                 "players": [{
                     "nick": "acidburn",
                     "number": 1
                 }],
                 "player_won": null,
                 "last_gamble": null,
                 "player_turn": 1,
                 "id": 123,
                 "round": 1
             }
         }


- Each participant should set their pusher to the channel "fivedice.game.123"
  (where 123 is the ID for your game)


- Somebody else joins the game (note, this example needs 3 people before it
  starts)

      POST /game/123/join {"nick": "zerocool"}
      # IN THE GAME!
      ~> {
             "game_url": "http://localhost:8000/game/123/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
             "player": {
                 "nick": "zerocool",
                 "secret": "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                 "number": 2
             },
             "game": {
                 "num_players": 3,
                 "status": 1,
                 "players": [{
                     "nick": "acidburn",
                     "number": 1
                 }, {
                     "nick": "zerocool",
                     "number": 2
                 }],
                 "player_won": null,
                 "last_gamble": null,
                 "player_turn": 1,
                 "id": 123,
                 "round": 1
             }
         }
      # GAME FULL
      ~> {"error": "Sorry mate, that game has started"}


- Once a third joins the game is full and it begins. A pusher message is sent
  to everyone on the channel fivedice.game.123 with first "game state event".

      # FIRST ROUND, IT'S PLAYER ONES TURN
      ~> {"game": {"round": 1, "player_turn": 1, ..}, ..}


- Everyone fetches their state from the server, for example here is player 1's
  NOTE: Repeat hits to fetch state will return the same result until the next
  round

      GET /game/123/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      ~> {"player": {"nick": "acidburn", "number": 1, "dice": "1,4,5,4,3", ..}, ..}



- Player 1's turn, they make their move

      POST /game/123/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/do_turn

  Example POST data:

      gamble=2,3       # SAY "I think there are at least TWO THREES"
      gamble=bullshit  # CALL BULLSHIT
      gamble=exact     # CALL EXACT on the previous gamble

  Example responses:

      ~> {"error": "It's not your turn!"}
      ~> {"error": "Either the number of dice or the value must go up!"}
      ~> {"error": "You can't call bullshit on the first turn of the round!"}
      ~> {"error": "You can't call exact on the first turn of the round!"}


- Server calculates the result and updates game state. A push is sent out
  giving everyone new game state.

      # IT'S PLAYER TWO'S TURN, etc.
      ~> {"game": {"round": 1, "player_turn": 2, "last_gamble": "2,5", ..} ..}


- Everyone fetches their roll


- Player 2's turn, they make their move

      POST /game/123/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB/do_turn  gamble=bullshit


- Server calculates the result and updates game state. A push is sent out
  giving everyone new game state. Uhoh, looks like player 2 lost that round.
  It's now players 2's turn to make the first call. Note we are now on
  round 2.

      ~> {"game": {"round": 2, "player_turn": 2, "last_loser": 2, ..}, ..}


- Everyone fetches their roll from the server, for example here is player 2's
  Note that player 2 is now down one dice!

      GET /game/123/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
      ~> {"player": {"nick": "zerocool", "number": 1, "dice": "6,2,1,1", ..}, ..}


- Player 2's turn, they make their move

      POST /game/123/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB/do_turn  gamble=2,1


- Game state is calculated and sent via pusher..

      ~> {"game": {"round": 2, "player_turn": 3, "last_gamble": "2,1", ..}, ..}


- Player 3's turn finally

      POST /game/123/CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC/do_turn  gamble=3,1
      ~> {"game": {"round": 2, "player_turn": 1, "last_gamble": "3,1", ..}, ..}


- Game state is calculated and sent via pusher..


- Player 1's turn again. They call exact and get it right!! Note we are now
  on round 3.

      POST /game/123/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/do_turn  gamble=exact
      ~> {"game": {"round": 2, "player_turn": 1, "last_loser": 3, ..}, ..}


- Game keeps on going in the manner. Until someone loses all of their dice.
  This sad news arrives to everyone via pusher. Looks like player 2 is out
  of the game. Any calls they make to the API will be
  met with an error: {"error": "Sorry mate, you're out."}. Player 2 is still
  welcome to keep connected to the pusher game state channel and watch the
  remainder of the game.

      ~> {"game": {"round": 333, "player_turn": 1, "last_loser": 2, ..}, ..}


- The game continues until only one player remains then everyone is notified
  via pusher of the victory. After this point the game is archived. All calls
  to the API will be met with an error: {"error": "Sorry mate, game over."}

      ~> {"game": {"round": 999, "player_won": 1, ..}, ..}


- Optionally if a player wishes to bail on the game they may ping the "quit"
  endpoint.

      POST /game/123/quit
      ~> true
      ~> {"error": "I can't imagine what would go wrong."}

  This will update the game state and everyone will receive a pusher
  notification about this.

      ~> {"game": {"round": 999, "player_quit": 1, ..}, ..}

