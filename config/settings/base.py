"""Django settings for taxinnovation project."""
from datetime import timedelta

import environ
from corsheaders.defaults import default_headers
from google.oauth2 import service_account

BASE_DIR = environ.Path(__file__) - 3
PROJECT_DIR = BASE_DIR.path('taxinnovation')
APPS_DIR = PROJECT_DIR.path('apps')

env = environ.Env()

# Base
DEBUG = env.bool('DJANGO_DEBUG', False)
GCP_FILES = env.bool('GCP_FILES', True)
SECRET_KEY = env('DJANGO_SECRET_KEY', default='fo*_7tyt9l7yk(636-240rmnujdodw2*+8t!1@s@cgruqmjhed')

# Language and timezone
TIME_ZONE = 'America/Mexico_City'
LANGUAGE_CODE = 'es-mx'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('POSTGRES_HOST'),
        'PORT': env.str('POSTGRES_PORT'),
        'TEST': {
            'NAME': env.str('POSTGRES_DB_TEST', 'test_tax_innovation'),
        },
    }
}
DATABASES['default']['ATOMIC_REQUESTS'] = True  # NOQA
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=60)  # NOQA

# URLs
ROOT_URLCONF = 'config.urls'

# WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# Users & Authentication
AUTH_USER_MODEL = 'users.User'

# Apps
DJANGO_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites'
]

THIRD_APPS = [
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'bulk_update_or_create',
]

LOCAL_APPS = [
    'taxinnovation.apps.utils.apps.UtilsAppConfig',
    'taxinnovation.apps.users.apps.UsersAppConfig',
    'taxinnovation.apps.catalogs.apps.CatalogsAppConfig',
    'taxinnovation.apps.listo_api.apps.ListoApiAppConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + LOCAL_APPS

# Security
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# PASSWORD HASHERS
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        # If you use MultiPartFormParser or FormParser, we also have a camel case version
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "config.core.pagination.CustomPagination",
    "DEFAULT_FILTER_BACKENDS": [
        "url_filter.integrations.drf.DjangoFilterBackend",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "PAGE_SIZE": 999,
    "EXCEPTION_HANDLER": "rest_framework_friendly_errors.handlers.friendly_exception_handler",
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M",
}

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = str(BASE_DIR('staticfiles'))
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    PROJECT_DIR('static')
]
# Media
MEDIA_ROOT = str(PROJECT_DIR('media'))
MEDIA_URL = '/media/'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(PROJECT_DIR.path('templates')),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

DEFAULT_FROM_EMAIL = env(
    'DJANGO_DEFAULT_FROM_EMAIL',
    default='TAX INNOVATION <noreply@fygproducts.com>'
)
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)
EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[TAX INNOVATION]')

# Email settings smtp
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# Admin
ADMIN_URL = env('DJANGO_ADMIN_URL', default='admin/')

#Listo Api
LISTO_MASTER_TOKEN = env('LISTO_MASTER_TOKEN', default='')

# Admin
ADMINS = [
    ("""Ramses Martinez""", 'ramses.martinez@fygsolutions.com'),
]
MANAGERS = ADMINS

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    'strict-origin-when-cross-origin',
]

# GRAPPELLI SETTINGS
# ------------------------------------------------------------------------------
GRAPPELLI_ADMIN_TITLE = "tax-innovation"
GRAPPELLI_SWITCH_USER = True

if GCP_FILES:
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
