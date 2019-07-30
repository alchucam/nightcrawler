from django.core.management.base import BaseCommand, CommandError
from nightcrawler.apps.services.models import *

class Command(BaseCommand):
    help = 'delete old datas that are more than 7 days'

    def handle(self, *args, **options):
        print("Start deletion tasks")
        delete_newsData = newsData.objects.filter(date__lte=timezone.now() - timedelta(days=7))
        if delete_newsData.exists():
            delete_newsData.delete()
            print("deleting newsData is successful")
        else:
            print("no newsData to delete")
        print("Finish custom periodic tasks")

        delete_collectedData = collectedData.objects.filter(date__lte=timezone.now() - timedelta(days=7))
        if delete_collectedData.exists():
            delete_collectedData.delete()
            print("deleting collectedData is successful")
        else:
            print("no collectedData to delete")
        print("Finish custom periodic tasks")
            
        

#for periodic schedule task
