from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from datetime import datetime 
from datetime import timedelta

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptostrat_project.settings')

app = Celery('cryptostrat_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.worker_concurrency = 1
app.conf.timezone = 'Europe/London'
app.conf.worker_prefetch_multiplier = 1

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    'localbitcoins_refresh_pending_and_disputed_transactions_statusess': {
        'task': 'localbitcoins_refresh_pending_and_disputed_transactions_statuses',
        'schedule': (30.0),
        #'args': []
    },
    'localbitcoins_process_pending_transactions': {
        'task': 'localbitcoins_process_pending_transactions',
        'schedule': (30.0),
        'options': {
            'expires': 120
        }
        #'args': []
    },
    'reference_price_update_gbpbtc_price': {
        'task': 'reference_price_update_gbpbtc_price',
        'schedule': (6.0),
        #'args': []
    },
    'get_localbitcoins_notifications': {
        'task': 'update_localbitcoins_notifications',
        'schedule': (10.0),
        'options': {
            'expires': 40
        }
        #'args': []
    },
    
}



