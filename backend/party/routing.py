from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/party/(?P<room_name>\w+)/$", consumers.PartyConsumer.as_asgi()),
]