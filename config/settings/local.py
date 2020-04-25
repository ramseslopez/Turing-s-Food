"""Development settings."""

from .base import *  # NOQA
from .base import env

# Base
DEBUG = env.bool('DJANGO_DEBUG', True)

# Security

SECRET_KEY = env(
    'DJANGO_SECRET_KEY',
    default='4ra7dxrd(&tmw$b5s9--akuakuisreal0v4!!f_-h7i)b_96aw'
)

ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',
    '127.0.0.1',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tfood',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Templates

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Development apps

INSTALLED_APPS += [
    'django_extensions',
]

# Security

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
