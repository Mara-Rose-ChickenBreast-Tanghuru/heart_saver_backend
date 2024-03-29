"""
ASGI config for heart project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import location.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heart.settings')

application = ProtocolTypeRouter({
    # http handler
    "http": get_asgi_application(),
    # websocket handler
    "websocket": AuthMiddlewareStack(
        URLRouter(
            location.routing.websocket_urlpatterns
        )
    )
})