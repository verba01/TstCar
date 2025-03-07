import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from crypto_app.crypto.consumers import BinanceConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_app.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/prices/', BinanceConsumer.as_asgi()),
        ])
    ),
})