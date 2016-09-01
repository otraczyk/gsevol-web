import os
import django
from celery import Celery

# Celery settings

# Whether celery and websockets should be used for delivering computation results.
# May be disabled for development.
DELEGATE_TASKS = True
# DELEGATE_TASKS = False

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

django.setup()

app = Celery('gsevol')

app.conf.update(
    BROKER_URL = 'redis://localhost/',
    CELERY_RESULT_BACKEND = "redis://localhost/",
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack'],
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json'
)

app.autodiscover_tasks(lambda: ['bindings'])
