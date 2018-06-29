from apscheduler.schedulers.blocking import BlockingScheduler
from nightcrawler.apps.services.models import *

#for custom periodic tasks
#delete old data that is more than 8 days.

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=1)
def timed_job_testing():
    print('This job is run every thirty minutes.')

#@sched.scheduled_job('interval', days=8)
@sched.scheduled_job('interval', minutes=10)
def delete_old_data():
    print("deleting old data...")
    newsData.delete_old()
    collectedData.delete_old()
    print("delete finished!")

sched.start()
