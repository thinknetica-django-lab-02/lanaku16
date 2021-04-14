import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')

app = Celery('marketplace')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    # Executes every Monday morning at 12:00 a.m.
    'add-every-monday-morning': {
        'task': 'main.tasks.monday_mail_about_new_goods',
        'schedule': crontab(minute='0', hour='12', day_of_week='sun')
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
