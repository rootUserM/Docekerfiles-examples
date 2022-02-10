from .base import *  # NOQA
from .base import env

# Base
DEBUG = True

# Security
ALLOWED_HOSTS = [
    "*",
]

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG   # NOQA

# Django Debug Toolbar
INSTALLED_APPS += [  # noqa F405
    'debug_toolbar',
]
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware', ] + MIDDLEWARE  # noqa F405

# GRAPH MODELS
GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}


# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST', default='localhost')
EMAIL_PORT = env('EMAIL_PORT', default=1025)

# django-extensions
INSTALLED_APPS += ['django_extensions']  # noqa F405

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
        'db_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/taxinnovation.db.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', ],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'propagate': False,
            'handlers': ['db_handler']
        }
    }
}
