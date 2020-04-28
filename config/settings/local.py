"""Development settings."""

from .base import *  # NOQA
from .base import env

# Base
environ.Env.read_env(os.path.join(BASE_DIR, '.env')) # This reads `.env` file variables
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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

# Email
EMAIL_HOST_USER = env('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('DJANGO_EMAIL_HOST_PASSWORD')
