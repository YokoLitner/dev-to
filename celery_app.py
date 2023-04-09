from celery.schedules import crontab
from django.conf import settings
from celery import Celery
import os
# from articles.tasks import load_articles

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings')
app.conf.broker__url = settings.BROKER_URL
app.autodiscover_tasks()
app.conf.timezone = 'UTC'


app.conf.beat_schedule = {
    'load-articles-every-day': {
        'task': 'articles.tasks.load_articles',
        'schedule':  crontab(hour=1),
    },
}
