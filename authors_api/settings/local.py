from .base import *
from .base import env


SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="LdmtB0GjN6zhqsYjE9L9pyn9Sc7cmsh_mpo5a-1GCD_DEL0RuPM"
)

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080", "http://127.0.0.1:8080"]

DEBUG = True

ALLOWED_HOSTS = []