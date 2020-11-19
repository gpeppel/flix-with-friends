import flask_socketio

from socketns.base import BaseNamespace
from socketns.youtube import YoutubeNamespace


class CustomCombinedNamespace(flask_socketio.Namespace):
    def __init__(self, namespace, server, namespace_objects):
        super().__init__(namespace)
        self.namespace = namespace
        self.flaskserver = server

        for obj in namespace_objects:
            events = list(filter(
                lambda x: x.startswith('on_') and callable(getattr(obj, x)),
                dir(obj)
            ))

            for ev in events:
                setattr(self, ev, getattr(obj, ev))
