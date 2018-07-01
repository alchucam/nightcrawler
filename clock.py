from unipath import Path
import sys
import os


PROJECT_DIR = Path(os.path.abspath(__file__))
sys.path.append(PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nightcrawler.settings')

import django
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler
from nightcrawler.apps.services.models import *
from django.utils import timezone
from datetime import timedelta

#for custom periodic tasks
#delete old data that is more than 7 days.

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=40)
def ping():
    print("i'm still alive!")


#@sched.scheduled_job('interval', days=1)
@sched.scheduled_job('cron', timezone='UTC', hour=0)
def delete_old_data():
    print("Start custom periodic tasks. Run at 00:00 UTC")
    delete_newsData = newsData.objects.filter(date__lte=timezone.now() - timedelta(days=7))
    if delete_newsData.exists():
        delete_newsData.delete()
        print("delete successful")
    else:
        print("delete fail")
    print("Finish custom periodic tasks")


sched.start()
