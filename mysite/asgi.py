# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chatapp.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # This handles HTTP requests
    "websocket": AuthMiddlewareStack(  # This handles WebSocket requests
        URLRouter(
            websocket_urlpatterns  # Include the WebSocket URL patterns
        )
    ),
})
