from config.settings.os_env import SECRET_KEY
from .base import *

SECRET_KEY = SECRET_KEY

DEBUG = True

ALLOWED_HOSTS = [
    'localhost'
    ]

CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:13000',
    'http://localhost:13000',
]

MEDIA_URL = '/media/'

