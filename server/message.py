from django.conf import settings
from pusher import Pusher


def send(channel, event, data, socket_id=None):
    """
    Sends a message to all connected clients.

    Args:
        channel   (str): The channel to send this message on. Think of it as an
                         "event group" or "event type".
        event     (str): The event name to send. Used by clients to distinguish
                         between events.
        data     (dict): The data to send
        socket_id (str): Optional, a client socket ID to EXCLUDE from the
                         recipients list. Used to avoid an event originator
                         from receiving an echo of its own events.
    """
    p = Pusher(
        app_id=settings.PUSHER_APP_ID,
        key=settings.PUSHER_KEY,
        secret=settings.PUSHER_SECRET)
    c = settings.PUSHER_CHANNEL_BASE + '.' + channel
    return p[c].trigger(event, data, socket_id=socket_id)
