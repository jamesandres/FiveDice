WAITING_FOR_PLAYERS = 1
RUNNING = 2
OVER = 3

GAME_STATUSES = (
    (WAITING_FOR_PLAYERS, u"Waiting for players"),
    (RUNNING, u"Game running now"),
    (OVER, u"Game over"),
)


PLAYING = 1
QUIT = 2
LOST = 3
WON = 4

PLAYER_STATUSES = (
    (PLAYING, "Playing"),
    (QUIT, "Quit"),
    (LOST, "Lost"),
    (WON, "Won"),
)


def split_ints(string):
    if not string:
        return []
    else:
        return map(int, string.split(','))
