import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse

from server import WAITING_FOR_PLAYERS, RUNNING, OVER, PLAYING, QUIT, LOST, WON

from server.models import Game, Player


def _json_response(data):
    return HttpResponse(json.dumps(data), content_type="application/json")


def _json_error(msg):
    return HttpResponse(
        json.dumps({"error": msg}), content_type="application/json")


def game_list(request):
    if request.method.upper() not in ["GET"]:
        return HttpResponseBadRequest()

    return _json_response({
        "games": [
            g.to_dict()
            for g in Game.objects.filter(
                status__in=[WAITING_FOR_PLAYERS]).order_by('id')
        ]
    })


def game_rankings(request):
    if request.method.upper() not in ["GET"]:
        return HttpResponseBadRequest()

    return _json_error("Not implemented yet.")


def game_new(request):
    if request.method.upper() not in ["POST"]:
        return HttpResponseBadRequest()

    num_players = request.POST.get("num_players", None)
    nick = request.POST.get("nick", None)

    if not num_players:
        return _json_error("'num_players' field is required.")
    if not nick:
        return _json_error("'nick' field is required.")

    game = Game(num_players=num_players)
    game.save()

    player = Player(nick=nick, secret=Player.generate_secret(), game=game)
    player.save()

    return _json_response({
        "game": game.to_dict(),
        "player": player.to_dict(show_secret=True),
        "game_url": request.build_absolute_uri(reverse(
            "game-player-state",
            kwargs={"pk": game.pk, "secret": player.secret})),
    })


def game_state(request, pk):
    if request.method.upper() not in ["GET"]:
        return HttpResponseBadRequest()

    game = Game.objects.get(pk=pk)

    return _json_response({"game": game.to_dict()})


def game_join(request, pk):
    if request.method.upper() not in ["POST"]:
        return HttpResponseBadRequest()

    game = Game.objects.get(pk=pk)

    if game.status != WAITING_FOR_PLAYERS:
        return _json_error("Sorry mate, that game has started")

    nick = request.POST.get("nick", None)
    if not nick:
        return _json_error("'nick' field is required.")

    if game.player_set.filter(nick=nick).exists():
        return _json_error("'nick' %s already taken" % nick)

    player = Player(nick=nick, secret=Player.generate_secret(), game=game)
    player.save()

    if game.player_set.count() >= game.num_players:
        game.status = RUNNING
        game.save()

    return _json_response({
        "game": game.to_dict(),
        "player": player.to_dict(show_secret=True),
        "game_url": request.build_absolute_uri(reverse(
            "game-player-state",
            kwargs={"pk": game.pk, "secret": player.secret})),
    })


def game_player_state(request, pk, secret):
    if request.method.upper() not in ["GET"]:
        return HttpResponseBadRequest()

    game = Game.objects.get(pk=pk)
    player = game.player_set.get(secret=secret, state=PLAYING)

    return _json_response({
        "game": game.to_dict(),
        "player": player.to_dict(show_dice=True)
    })


def game_do_turn(request, pk, secret):
    if request.method.upper() not in ["POST"]:
        return HttpResponseBadRequest()

    game = Game.objects.get(pk=pk)
    player = game.player_set.get(secret=secret, state=PLAYING)

    return _json_error("Not implemented yet.")


def game_quit(request, pk, secret):
    if request.method.upper() not in ["POST"]:
        return HttpResponseBadRequest()

    game = Game.objects.get(pk=pk)
    player = game.player_set.get(secret=secret, state=PLAYING)

    player.state = QUIT
    player.save()

    return _json_response(True)
