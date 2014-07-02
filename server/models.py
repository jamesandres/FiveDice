import os
import random

from django.db import models

from server import (
    GAME_STATUSES, WAITING_FOR_PLAYERS, PLAYER_STATUSES, PLAYING, LOST, WON,
    split_ints)


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
    def playing_players(self):
        return self.player_set.filter(status=PLAYING)

    @property
    def players(self):
        return self.playing_players.order_by('number')

    @property
    def current_player(self):
        return self.playing_players.get(number=self.player_turn)

    @property
    def count_dice_for_all_players(self):
        totals = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        for p in self.playing_players:
            dice = split_ints(p.dice)
            for v in dice:
                totals[v] += 1

        # Return the totals minus any empties
        return {k: v for k, v in totals.items() if v > 0}

    def generate_next_player_number(self):
        p = list(self.players)
        return p[-1].number + 1 if p else 1

    def roll_all_dice(self):
        for player in self.player_set.filter(status=PLAYING):
            player.roll_dice()

    def next_player_number(self):
        return (self.player_turn % self.num_players) + 1

    def prev_player_number(self):
        return (self.num_players + self.player_turn - 2) % self.num_players + 1

    def do_gamble(self, gamble):
        self.last_gamble = gamble
        self.player_turn = self.next_player_number()
        self.save()

    def do_exact(self):
        player = self.current_player
        num_dice, value_called = split_ints(self.last_gamble)
        totals = self.count_dice_for_all_players

        if totals[value_called] == num_dice:
            loser = self.player_set.filter(number=self.prev_player_number)
            self.tally_round(player, loser, winner_gains_die=True)
        else:
            winner = self.player_set.filter(number=self.prev_player_number)
            self.tally_round(winner, player)

    def do_bullshit(self):
        player = self.current_player
        num_dice, value_called = split_ints(self.last_gamble)
        totals = self.count_dice_for_all_players

        if totals[value_called] < num_dice:
            loser = self.player_set.filter(number=self.prev_player_number)
            self.tally_round(player, loser)
        else:
            winner = self.player_set.filter(number=self.prev_player_number)
            self.tally_round(winner, player)

    def tally_round(winner, loser, winner_gains_die=False):
        loser.lost_round()

        if winner_gains_die:
            winner.gain_a_die()

        if self.playing_players.count() == 1:
            self.player_won = winner.number
            self.status = OVER
        else:
            self.round += 1
            self.player_turn = loser.number
        self.save()

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
        self.dice = ','.join([str(random.randint(1, 6)) for i in range(5)])
        self.save()

    def lost_round(self):
        dice = split_ints(self.dice)

        if len(dice) <= 0:
            self.dice = ''
            self.status = LOST
        else:
            self.dice = ','.join(dice[:-1])
        self.save()

    def gain_a_die(self):
        dice = split_ints(self.dice)

        if len(dice) < 5:
            self.dice = ','.join(dice + [1])
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
