from settings.base import *

DEBUG = False

TEMPLATE_DEBUG = False

if os.environ['DJANGO_SETTINGS_MODULE'] == 'settings.production':
    from settings.celeryapp import *
