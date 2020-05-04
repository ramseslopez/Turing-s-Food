"""Development settings."""

from .base import *  # NOQA
from .base import env

# Base
DEBUG = True

# Security

SECRET_KEY = 'test'

ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',
    '127.0.0.1',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
