import os

from django.db import models

from server import GAME_STATUSES, WAITING_FOR_PLAYERS


def xstr(s):
    if s is None:
        return ''
    else:
        return str(s)


class Game(models.Model):
    # The number of player who must join before this game will begin
    num_players = models.SmallIntegerField()

    # Denormalised field to easily look up games waiting for players
    status = models.SmallIntegerField(
        choices=GAME_STATUSES, default=WAITING_FOR_PLAYERS)

    # Using the player turn number here rather than foreign key references.
    # Slightly slower maybe but it is a relative value and avoids accidentally
    # referencing players who are not meant to be in this game.
    player_turn = models.SmallIntegerField(default=1)
    player_won = models.SmallIntegerField(blank=True, null=True, default=None)

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "player_turn": self.player_turn,
            "player_won": self.player_won,
        }

    def __str__(self):
        return '<Game #' + self.id + ': ,'.join([
            xstr(self.num_players),
            xstr(self.status),
            xstr(self.player_turn),
            xstr(self.player_won),
        ]) + '>'


class Player(models.Model):
    """
    This object is best thought of as Player Game State. It is a combination
    of all three and simplifies the architecture somewhat. There is no sign-up,
    registration, or login with this architecture. Just supply a nick and you
    are in (assuming the game isn't full).
    """
    nick = models.CharField(max_length=32)
    number = models.SmallIntegerField(default=1)
    secret = models.CharField(max_length=64)
    game = models.ForeignKey(Game)
    dice = models.CommaSeparatedIntegerField(max_length=32, default="1,1,1,1,1")

    @staticmethod
    def generate_secret():
        return os.urandom(16).encode('hex')

    def to_dict(self, show_secret=False):
        data = {
            "nick": self.nick,
            "number": self.number,
            "dice": self.dice,
        }
        if show_secret:
            data["secret"] = self.secret
        return data

    def __str__(self):
        return '<Game #' + self.id + ': ,'.join([
            xstr(self.nick),
            xstr(self.number),
            xstr(self.secret),
            xstr(self.game),
            xstr(self.dice),
        ]) + '>'
