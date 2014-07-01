import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse

from server import WAITING_FOR_PLAYERS, RUNNING, OVER

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
            'game-base', kwargs={"pk": game.pk, "secret": player.secret})),
    })


def game_join(request, pk):
    if request.method.upper() not in ["POST"]:
        return HttpResponseBadRequest()

    return _json_error("Not implemented yet.")


def game_state(request, pk, secret=None):
    if request.method.upper() not in ["GET"]:
        return HttpResponseBadRequest()

    return _json_error("Not implemented yet.")


def game_get_roll(request, pk, secret):
    if request.method.upper() not in ["GET"]:
        return HttpResponseBadRequest()

    return _json_error("Not implemented yet.")


def game_do_turn(request, pk, secret):
    if request.method.upper() not in ["POST"]:
        return HttpResponseBadRequest()

    return _json_error("Not implemented yet.")


def game_quit(request, pk, secret):
    if request.method.upper() not in ["POST"]:
        return HttpResponseBadRequest()

    return _json_error("Not implemented yet.")
