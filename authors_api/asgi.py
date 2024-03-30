import os

from django.core.asgi import get_asgi_application

# TODO change this in production!
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "authors_api.settings.local")

application = get_asgi_application()
