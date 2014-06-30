# FiveDice Game Reenactment

- First player creates a new game and implicitly joins it as the first
  participant. The server sends them their player number and a unique game
  URL with an embedded token that identifies the player for each request
  Security! ;-)

      POST /game/new {"num_players": 3, "nick": "acidburn"}
      ~> {
             "player_id": 1,
             "game_id": 123,
             "game_url": "http://1.2.3.4/game/123/AAAAAAAAAAAAAAAA"
         }

- Each participant should set their pusher to the channel "game:123" (where
  123 is the ID for your game)

- Somebody else joins the game (note, this example needs 3 people before it
  starts)

      POST /game/123/join {"nick": "zerocool"}
      ~> {"game_url": "http://1.2.3.4/game/123/BBBBBBBBBBBBBBBB"}  # IN THE GAME!
      ~> {"error": "Sorry that game has started"}                  # GAME FULL

- Once a third joins the game is full and it begins. A pusher message is sent
  to everyone on the channel game:123 with first "game state event".

      ~> {"round": 1, "player_turn": 1}  # IT'S PLAYER ONES TURN

- Everyone fetches their roll from the server, for example here is player 1's
  NOTE: Repeat hits to "roll" will return the same result until the next round

      GET /game/123/AAAAAAAAAAAAAAAA/roll
      ~> {"dice": [1, 5, 3, 3, 2]}


- Player 1's turn, they make their move

      POST /game/123/AAAAAAAAAAAAAAAA/do_turn

  Example POST data:

      {"gamble": [2, 3]}      # SAY "I think there are at least TWO THREES"
      {"gamble": "bullshit"}  # CALL BULLSHIT
      {"gamble": "exact"}     # CALL EXACT on the previous gamble

  Example responses:

      ~> {"error": "You have not fetched your roll yet. Foolish!"}
      ~> {"error": "It's not your turn!"}
      ~> {"error": "Either the number of dice or the value must go up!"}
      ~> {"error": "You can't call bullshit on the first turn of the round!"}
      ~> {"error": "You can't call exact on the first turn of the round!"}

- Server calculates the result and updates game state. A push is sent out
  giving everyone new game state.

      ~> {"round": 1, "player_turn": 2, "gamble": [2, 5]}  # IT'S PLAYER TWO'S TURN, etc.

- Everyone fetches their roll

- Player 2's turn, they make their move

      POST /game/123/BBBBBBBBBBBBBBBB/do_turn  {"gamble": "bullshit"}

- Server calculates the result and updates game state. A push is sent out
  giving everyone new game state. Uhoh, looks like player 2 lost that round.
  It's now players 2's turn to make the first call. Note we are now on
  round 2.

      ~> {"round": 2, "player_turn": 2, "player_wrong": 2}

- Everyone fetches their roll from the server, for example here is player 2's
  Note that player 2 is now down one dice!

      GET /game/123/AAAAAAAAAAAAAAAA/roll
      ~> {"dice": [6, 2, 1, 1]}

- Player 2's turn, they make their move

      POST /game/123/BBBBBBBBBBBBBBBB/do_turn  {"gamble": [2, 1]}

- Game state is calculated and sent via pusher..

      ~> {"round": 2, "player_turn": 3, "gamble": [2, 1]}

- Player 3's turn finally

      POST /game/123/CCCCCCCCCCCCCCCC/do_turn  {"gamble": [3, 1]}
      ~> {"round": 2, "player_turn": 1, "gamble": [3, 1]}

- Game state is calculated and sent via pusher..

- Player 1's turn again. They call exact and get it right!! Note we are now
  on round 3.

      POST /game/123/AAAAAAAAAAAAAAAA/do_turn  {"gamble": "exact"}
      ~> {"round": 3, "player_turn": 1, "player_exact": 1}

- Game keeps on going in the manner. Until someone loses all of their dice.
  This sad news arrives to everyone via pusher. Looks like player 2 is out
  of the game. Any calls they make to the API will be
  met with an error: {"error": "Sorry mate, you're out."}. Player 2 is still
  welcome to keep connected to the pusher game state channel and watch the
  remainder of the game.

      ~> {"round": 333, "player_turn": 1, "player_wrong": 2, "player_out": 2}

- The game continues until only one player remains then everyone is notified
  via pusher of the victory. After this point the game is archived. All calls
  to the API will be met with an error: {"error": "Sorry mate, game over."}

      ~> {"round": 999, "player_won": 1}

- Optionally if a player wishes to bail on the game they may ping the "quit"
  endpoint.

      POST /game/123/quit
      ~> true
      ~> {"error": "I can't imagine what would go wrong."}

  This will update the game state and everyone will receive a pusher
  notification about this.

      ~> {"round": 123, "player_quit": 2}

