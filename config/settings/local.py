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
SENDGRID_SANDBOX_MODE_IN_DEBUG = True
SENDGRID_ECHO_TO_STDOUT=True

# Google Cloud
GOOGLE_CLOUD_API_KEY = env('GOOGLE_CLOUD_API_KEY')

# Stripe
STRIPE_API_KEY = env('STRIPE_API_KEY')
STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY')
