# chat/routing.py
from django.urls import re_path

from .consumers import GamePlayConsumer

websocket_urlpatterns = [
    re_path(r"ws/gameplay/$", GamePlayConsumer.as_asgi()),
]