import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import transcript.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stream.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            transcript.routing.websocket_urlpatterns
        )
    ),
})