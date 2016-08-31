"""
Django settings for gsevol project.

"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y#ak@x81+wt(igl*h7z60@q_@+#!@@2+0j8(g3d^&w5x1yd-cb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
   # 'django.contrib.admin',
   # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'ws4redis',
    'api',
    'front',
    'bindings',
    'styling',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WEBSOCKET_URL = '/ws/'
WS4REDIS_PREFIX = 'ws'
WSGI_APPLICATION = 'ws4redis.django_runserver.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'ws4redis.context_processors.default',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT =  os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    'front/dist/',
)
if DEBUG:
        STATICFILES_DIRS += (
            'front/bower_components/',
            'front/build/',
            'front/assets'
        )

# Celery settings

# Whether celery and websockets should be used for delivering computation results.
# May be disabled for development.
DELEGATE_TASKS = True
# DELEGATE_TASKS = False

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from celery import Celery
app = Celery('gsevol')

app.conf.update(
    BROKER_URL = 'redis://localhost/',
    CELERY_RESULT_BACKEND = "redis://localhost/",
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack'],
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json'
)

app.autodiscover_tasks(lambda: INSTALLED_APPS)

# Local settings can overload values defined in this file.
# They should define:
# SECRET_KEY = ''
# ALLOWED_HOSTS = [] - for production setup
try:
    from .settings_local import *
except ImportError:
    pass
