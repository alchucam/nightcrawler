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

#for custom periodic tasks
#delete old data that is more than 8 days.

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def delete_old_data():
    print("Start custom periodic tasks")
    delete_newsData = newsData.objects.filter(date__day__gte=8)
    if delete_newsData.exists():
        print("delete successful")
        for delete in delete_newsData:
            print(delete.title)
    else:
        print("delete fail")
    print("Finish custom periodic tasks")

    print("Start custom periodic tasks")
    delete_newsData = newsData.objects.filter(date__day__lte=8)
    if delete_newsData.exists():
        print("delete successful")
        for delete in delete_newsData:
            print(delete.title)
    else:
        print("delete fail")
    print("Finish custom periodic tasks")

sched.start()
