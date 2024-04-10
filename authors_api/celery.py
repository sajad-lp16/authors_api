import os

from django.conf import settings

from celery import Celery


# TODO change this in Production
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "authors_api.settings.local")

app = Celery("authors_api")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
