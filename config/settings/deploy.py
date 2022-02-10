"""Production settings."""

from .base import *  # NOQA
from .base import env

# Base
ALLOWED_HOSTS = [
    "*",
]

# EMAILS
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Templates
TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    ),
]

# Gunicorn
INSTALLED_APPS += ["gunicorn"]  # noqa F405

# WhiteNoise
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")  # noqa F405

# Logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s\t[%(levelname)s]\t%(module)s\t%(process)d\t%(thread)d\t%(message)s"
        }
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/taxinnovation.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "request_handler": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/taxinnovation.request.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "loggers": {
        "": {"handlers": ["default"], "level": "DEBUG", "propagate": True},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["default", "mail_admins"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["request_handler", "mail_admins"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# Admin

ADMIN_URL = env("DJANGO_ADMIN_URL")
