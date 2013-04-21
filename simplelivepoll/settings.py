# Django settings for simplelivepoll project.
import mimetypes
import os

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
from django.core.urlresolvers import reverse_lazy
import django_cache_url
import dj_database_url
import djcelery


PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(PROJECT_DIR)

DEBUG = bool(os.environ.get('DEBUG', False))
DEVELOPMENT_SITE = bool(os.environ.get('DEVELOPMENT_SITE', False))

DATABASES = {'default': dj_database_url.config(default='postgres://localhost/simplelivepoll')}

CACHES = {'default': django_cache_url.config()}

ADMINS = (('Admin', 'james@incuna.com'),)
MANAGERS = ADMINS
ADMIN_EMAILS = zip(*ADMINS)[1]
EMAIL_SUBJECT_PREFIX = '[simplelivepoll] '
SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'james@incuna.com'
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

TIME_ZONE = 'UTC'
USE_L10N = True  # Locale
USE_TZ = True

LANGUAGE_CODE = 'en-GB'
USE_I18N = False  # Internationalization

# AWS
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_LOCATION = os.environ.get('AWS_LOCATION', '')
AWS_S3_SECURE_URLS = False
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'simplelivepoll')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
AWS_CLOUDFRONT_STREAMING_DOMAIN = os.environ.get('AWS_CLOUDFRONT_STREAMING_DOMAIN')
DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE', 'incuna_storages.backends.S3MediaStorage')
STATICFILES_STORAGE = os.environ.get('STATICFILES_STORAGE', 'incuna_storages.backends.S3StaticStorage')
S3_URL = 'http://{0}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)

# Static
MEDIA_ROOT = os.path.join(ROOT_DIR, 'client_media')
MEDIA_URL = '/client_media/'
STATICFILES_DIR = os.path.join(PROJECT_DIR, 'static')
STATICFILES_DIRS = (STATICFILES_DIR,)
STATIC_ROOT = os.path.join(ROOT_DIR, 'static_media')
STATIC_URL = os.environ.get('STATIC_URL', S3_URL + 'static/')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

CSS_DEBUG = os.environ.get('CSS_DEBUG', False)

mimetypes.add_type('text/x-component', '.htc')

TEMPLATE_DEBUG = DEBUG
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'never_cache_post.middleware.NeverCachePostMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'admin_sso.auth.DjangoSSOAuthBackend',
)
LOGIN_URL = reverse_lazy('auth_login')
LOGOUT_URL = reverse_lazy('auth_logout')
LOGIN_REDIRECT_URL = '/'

ROOT_URLCONF = 'simplelivepoll.urls'
SECRET_KEY = '*q@4xo+vp%%c@t$w+*1+$p2=kij4le--x8ld3*)5r+%1=jn7h+'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
SITE_ID = 1
WSGI_APPLICATION = 'simplelivepoll.wsgi.application'

INSTALLED_APPS = (
    # Project Apps
    'simplelivepoll',

    # Libraries
    'incuna_storages',

    'admin_sso',
    'crispy_forms',
    # 'queued_storage',
    # 'djcelery',  # For queued_storage
    # 'kombu.transport.django',  # For Celery Django database broker
    'south',
    'debug_toolbar',
    'django_extensions',
    'gunicorn',
    'raven.contrib.django',
    'never_cache_post',

    # Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },
    'filters': {
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}
    },
    'handlers': {
        'sentry': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'raven.contrib.django.handlers.SentryHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['sentry', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'incuna.default': {
            'handlers': ['sentry', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'sentry.errors': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propogate': True,
        },
    }
}

# Celery
djcelery.setup_loader()
BROKER_URL = os.environ.get('BROKER_URL', 'django://')

# Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
INTERNAL_IPS = ('127.0.0.1',)



# Sorl settings
THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_SUBDIR = '_thumbs'
THUMBNAIL_QUALITY = 95

# South
SOUTH_MIGRATION_MODULES = {
    'page': 'simplelivepoll.projectmigrations.page',
}
