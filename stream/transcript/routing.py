from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("listen/", consumers.TranscriptConsumer.as_asgi()),
]