from django.core.management.base import BaseCommand, CommandError
from nightcrawler.apps.services.updater import *

class Command(BaseCommand):
    help = 'update to models for display and analysis'


    def handle(self, *args, **options):
        print("Start handle")
        nytimesUpdater().save_to_models()
        yonhapUpdater().save_to_models()
        ecnsUpdater().save_to_models()
        japantimesUpdater().save_to_models()
        nytimesUpdater().save_to_analysis()
        yonhapUpdater().save_to_analysis()
        ecnsUpdater().save_to_analysis()
        japantimesUpdater().save_to_analysis()
        print("Done handle")

#for periodic schedule task
