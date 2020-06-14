"""Production settings."""

from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Base

SECRET_KEY = env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = env.list(
    var='DJANGO_ALLOWED_HOSTS',
    default=[
        '.herokuapp.com',
    ]
)

# Databases

DATABASES = {
    'default': env.db('DATABASE_URL'),
}

DATABASES['default'] = env.db('DATABASE_URL')
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=60)

# Security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True
)
SECURE_HSTS_PRELOAD = env.bool('DJANGO_SECURE_HSTS_PRELOAD', default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True
)


# Static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Templates
TEMPLATES[0]['OPTIONS']['loaders'] = [
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]

del TEMPLATES[0]['APP_DIRS']

# Gunicorn
INSTALLED_APPS += [
    'gunicorn'
]

# WhiteNoise
MIDDLEWARE.insert(4, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Dropbox
DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DROPBOX_OAUTH2_TOKEN = env('DROPBOX_OAUTH2_TOKEN')

# Sentry
sentry_sdk.init(
    dsn="https://de8c0e937d1642deb16a585a9f881495@o253191.ingest.sentry.io/5199405",
    integrations=[DjangoIntegration()],
    send_default_pii=True
)

# Email
EMAIL_HOST_USER = env('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('DJANGO_EMAIL_HOST_PASSWORD')

# Google Cloud
GOOGLE_CLOUD_API_KEY = env('GOOGLE_CLOUD_API_KEY')

# Stripe
STRIPE_API_KEY = env('STRIPE_API_KEY')
STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY')
