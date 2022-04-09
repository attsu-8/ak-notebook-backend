from config.settings.os_env import SECRET_KEY
from .base import *

SECRET_KEY = "django-insecure-hrexa0k$1&1s+$mdbzjn_q)!)p^3c6=3o+3wz_(a@8dkj#r1q+"

DEBUG = False

ALLOWED_HOSTS = [
    '*'
    ]

CORS_ORIGIN_WHITELIST = [
    'https://ak-notebook.com'
]