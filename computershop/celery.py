import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'computershop.settings')

app = Celery('computershop')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'products_rating_update': {
        'task': 'services.tasks.my_task',
        'schedule': 5
    }
}

app.conf.timezone = 'Europe/Kiev'

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
