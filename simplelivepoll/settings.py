# Django settings for simplelivepoll project.
import os

from django.core.urlresolvers import reverse_lazy
import django_cache_url
import dj_database_url


PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(PROJECT_DIR)

DEBUG = bool(os.environ.get('DEBUG', False))
DEVELOPMENT_SITE = bool(os.environ.get('DEVELOPMENT_SITE', False))

DATABASES = {'default': dj_database_url.config(default='postgres://localhost/simplelivepoll')}

CACHES = {'default': django_cache_url.config()}

ALLOWED_HOSTS = ['simplelivepoll.herokuapp.com']

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

# Static
MEDIA_ROOT = 'client_media'
MEDIA_URL = '/media/'
STATIC_ROOT = 'static_media'
STATIC_URL = '/static/'

TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (os.path.join(ROOT_DIR, 'templates'))

MIDDLEWARE_CLASSES = (
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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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
    'debug_toolbar',
    'django_extensions',
    'never_cache_post',
    'orderable',

    # Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)

SENTRY_DSN = os.environ.get('SENTRY_DSN')
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
        'simplelivepoll.default': {
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

# Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
INTERNAL_IPS = ('127.0.0.1',)
