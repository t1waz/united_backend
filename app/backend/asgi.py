"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

import django
from channels.routing import (
    URLRouter,
    ProtocolTypeRouter,
)
from django.core.asgi import get_asgi_application

from common.middlewares import RobotAuthMiddleware
from robots.urls import websocket_urlpatterns as robots_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')
django.setup()

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': RobotAuthMiddleware(URLRouter(robots_urlpatterns)),
    }
)
