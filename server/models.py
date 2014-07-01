import os
import random

from django.db import models

from server import GAME_STATUSES, WAITING_FOR_PLAYERS, PLAYER_STATUSES, PLAYING


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

    round = models.IntegerField(default=1)
    last_gamble = models.CharField(max_length=32)

    # Using the player turn number here rather than foreign key references.
    # Slightly slower maybe but it is a relative value and avoids accidentally
    # referencing players who are not meant to be in this game.
    player_turn = models.SmallIntegerField(default=1)
    player_won = models.SmallIntegerField(blank=True, null=True, default=None)

    @property
    def players(self):
        return self.player_set.order_by('number')

    def roll_all_dice(self):
        for player in self.player_set.filter(status=PLAYING):
            player.roll_dice()

    def to_dict(self):
        return {
            "id": self.id,
            "num_players": self.num_players,
            "status": self.status,
            "player_turn": self.player_turn,
            "player_won": self.player_won,
            "players": [p.to_dict() for p in self.players]
        }

    def __str__(self):
        return '#' + str(self.id)


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
    dice = models.CommaSeparatedIntegerField(max_length=32, default="0,0,0,0,0")

    # Denormalised field to make finding forfeiters, winners and losers easier
    status = models.SmallIntegerField(choices=PLAYER_STATUSES, default=PLAYING)

    @staticmethod
    def generate_secret():
        return os.urandom(16).encode('hex')

    def roll_dice(self):
        # Roll 5 six sided dice
        self.dice = ','.join([random.randint(1, 6) for i in range(5)])
        self.save()

    def to_dict(self, show_dice=False, show_secret=False):
        data = {
            "nick": self.nick,
            "number": self.number,
        }
        if show_dice:
            data["dice"] = self.dice
        if show_secret:
            data["secret"] = self.secret
        return data

    def __str__(self):
        return '#' + str(self.id) + ': ' + ', '.join([
            xstr(self.number),
            xstr(self.nick)
        ])
