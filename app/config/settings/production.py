from config.settings.os_env import SECRET_KEY
from .base import *

SECRET_KEY = SECRET_KEY

DEBUG = False

ALLOWED_HOSTS = [
    '*'
    ]

CORS_ORIGIN_WHITELIST = [
    'https://ak-notebook.com',
    'https://ak-notebook.com:10443',
]