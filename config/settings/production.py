"""Production settings."""

from .base import *  # NOQA
from .base import BASE_DIR
from .base import env
from google.oauth2 import service_account


# Base
SECRET_KEY = env('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['*']

# Databases
DATABASES['default'] = env.db('DATABASE_URL')  # NOQA
DATABASES['default']['ATOMIC_REQUESTS'] = True  # NOQA
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=60)  # NOQA

# Admin
ADMIN_URL = env('DJANGO_ADMIN_URL')

# EMAILS
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
print("EMAIL_BACKEND"+"-----produccion")
print(EMAIL_BACKEND)

# Security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
SECURE_HSTS_PRELOAD = env.bool('DJANGO_SECURE_HSTS_PRELOAD', default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool('DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)

# STORAGES
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/#installation
INSTALLED_APPS += ["storages"]  # noqa F405
GS_BUCKET_NAME = env("DJANGO_GCP_STORAGE_BUCKET_NAME", default="tax-innovation-prod")
GS_DEFAULT_ACL = "publicRead"
GS_PROJECT_ID = env("GS_PROJECT_ID", default="tax-innovation-produccion")

print(BASE_DIR.path('config') + 'gcs-service-account.json')
print(BASE_DIR.path('config') + '/gcs-service-account.json')

GS_CREDENTIALS_PATH = str(BASE_DIR.path('config') + 'gcs-service-account.json')

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(GS_CREDENTIALS_PATH)

# Static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_FILE_STORAGE = "taxinnovation.utils.storages.MediaRootGoogleCloudStorage"
MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"

# Templates
TEMPLATES[0]['OPTIONS']['loaders'] = [  # noqa F405
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]

# Gunicorn
INSTALLED_APPS += ['gunicorn']  # noqa F405

# WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # noqa F405


# Logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s\t[%(levelname)s]\t%(module)s\t%(process)d\t%(thread)d\t%(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/taxinnovation.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/taxinnovation.request.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['default', 'mail_admins'],
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
