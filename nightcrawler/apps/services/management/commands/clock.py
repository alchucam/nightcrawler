from django.core.management.base import BaseCommand, CommandError
from apscheduler.schedulers.blocking import BlockingScheduler
from nightcrawler.apps.services.models import *

#for custom periodic tasks
#delete old data that is more than 8 days.

class Command(BaseCommand):
    help = 'delete old data that is more than 7 days'

    def handle(self, *args, **options):
        print("calling custom command")
        sched = BlockingScheduler()
        @sched.scheduled_job('interval', minutes=10)
        def delete_old_data():
            print("Start custom periodic tasks")
            newsData.delete_old()
            collectedData.delete_old()
            print("Finish custom periodic tasks")
        sched.start()
        print("finish calling custom command")
