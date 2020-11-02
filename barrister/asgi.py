import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from django.core.asgi import get_asgi_application
import chat.routing

from chat.consumers import AdminChatConsumer, PublicChatConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application()

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            chat.routing.websocket_urlpatterns
        ])
    ),
})