import os,sys
from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from nightcrawler.apps.services.updater import *
from nightcrawler.apps.services.models import *

os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "nightcrawler.settings"

@periodic_task(run_every=crontab(hour="2"))
def keep_it():
    nytimesUpdater().save_to_models()
    yonhapUpdater().save_to_models()
    ecnsUpdater().save_to_models()
    japantimesUpdater().save_to_models()
    nytimesUpdater().save_to_analysis()
    yonhapUpdater().save_to_analysis()
    ecnsUpdater().save_to_analysis()
    japantimesUpdater().save_to_analysis()
