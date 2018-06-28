import os
from celery import Celery
import django
from django.conf import settings
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nightcrawler.settings')

#celery_app = Celery('nightcrawler.tasks.keep_it', broker=settings.CELERY_BROKER_URL)
celery_app = Celery('nightcrawler', broker=settings.CELERY_BROKER_URL)
celery_app.config_from_object('django.conf:settings')

celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#celery_app.autodiscover_tasks()

@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
