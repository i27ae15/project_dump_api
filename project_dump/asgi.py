"""
ASGI config for project_dump project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

from .wsgi import *  # add this line to top of your code

import os

from dotenv import load_dotenv

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import gameplay.routing
from channels.security.websocket import OriginValidator


load_dotenv()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_dump.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()


LOCAL_DEVELOPMENT = os.environ.get('LOCAL_DEVELOPMENT', 'FALSE')

# if LOCAL_DEVELOPMENT.upper() == 'TRUE' or LOCAL_DEVELOPMENT == '1':

#     application = ProtocolTypeRouter(
#         {
#             "http": django_asgi_app,
#             "websocket": AuthMiddlewareStack(URLRouter(gameplay.routing.websocket_urlpatterns))
#         }
#     )
# else:
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": OriginValidator(
            AuthMiddlewareStack(URLRouter(gameplay.routing.websocket_urlpatterns)),
            ["https://projectdumpapi-production.up.railway.app"],
        ),
    }
)
