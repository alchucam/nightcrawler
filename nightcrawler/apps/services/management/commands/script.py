from django.core.management.base import BaseCommand, CommandError
from nightcrawler.apps.services.models import *

class Command(BaseCommand):
    help = 'update to models for display and analysis'

    def handle(self, *args, **options):
        print("calling custom command")
        @sched.scheduled_job('interval', minutes=10)
        def delete_old_data():
            print("Start custom periodic tasks")
            newsData.delete_old()
            collectedData.delete_old()
            print("Finish custom periodic tasks")
        sched.start()
        print("finish calling custom command")
