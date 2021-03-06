import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path


from chat.consumers import PublicChatConsumer,ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'connectus.settings')

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path("public_chat/<room_id>/", PublicChatConsumer.as_asgi()),
                path("chat/<room_id>/", ChatConsumer.as_asgi()),
            ])
        )
    )
})