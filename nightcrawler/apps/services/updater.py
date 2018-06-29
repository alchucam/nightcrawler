# -*- coding: utf-8 -*-

from django.db.models import F
from nightcrawler.apps.services.models import *
from nightcrawler.apps.services import crawlers
from nightcrawler.apps.services.analyzer import *
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date

#save_to_models: save all the new articles into newsData model
#save_to_analysis: save all the analyzed data from the articles into collectedData model
class abstractBaseUpdater(object):
    def __init__(self, crawler, publisher, fromCountry):
        self.crawler = crawler
        self.publisher = publisher
        self.fromCountry = fromCountry

    def save_to_models(self):
        print("calling save_to_models with {}".format(self.publisher))
        top_stories = self.crawler.get_Contents() #all the titles and articles

        if not top_stories: #if get_Contents return empty dict. end the function
            return

        for key in top_stories: #gets the key, title
            try:
                if newsData.objects.get(title=key): #due to foreignkey reference
                    continue
            except ObjectDoesNotExist:

                newsData.objects.create(
                    publisher=self.publisher,
                    title = key,
                    url = top_stories[key]['url'],
                    dateStr = top_stories[key]['time'],
                    compound = top_stories[key]['compound'],
                    freqList = top_stories[key]['word_freq'],
                    isArticle = top_stories[key]['isArticle']) #create model objects



    def save_to_analysis(self):
        print("calling save_to_analysis with {}".format(self.fromCountry))
        today = timezone.now()
        dates = date(int(today.year), int(today.month), int(today.day))

        data = newsData.objects.filter(publisher=self.publisher, date=dates)
        analyzerObj = analyzer()
        to_country = (('USA'),('CHN'),('KOR'),('PRK'),('JPN'))
        dataExport = dict()
        average = 0

        for to_c in to_country:
            for datum in data:
                dataExport = analyzerObj.toRelationship(datum, to_c)
                try: #if the query already exists. add appropriate ID to the list.
                    check = collectedData.objects.get(fromCountry = self.fromCountry, toCountry = to_c, date=dates)
                    if dataExport['toCheck'] and dataExport['toID'] not in check.toID: #when the searched collectedData exists, but the dataExport data has not been entered.

                        check.toCheck = dataExport['toCheck']
                        check.to_num += dataExport['to_num']
                        check.total_num = analyzerObj.total_articles(self.publisher)
                        if check.toID is "":
                            check.toID = dataExport['toID']
                        else:
                            check.toID += " " + dataExport['toID']
                        check.sumcompound += dataExport['compoundSum']
                        check.avgcompound = check.sumcompound/check.to_num
                        check.save()


                except ObjectDoesNotExist: #when the searched collectedData doesn't exists, and the dataExport data has not been entered.

                    if dataExport['to_num'] is not 0:
                        average = dataExport['compoundSum']/dataExport['to_num']
                    else:
                        average = 0
                    update = collectedData.objects.create(
                        fromCountry = self.fromCountry,
                        total_num = analyzerObj.total_articles(self.publisher),
                        to_num = dataExport['to_num'],
                        toCountry = to_c,
                        toCheck = dataExport['toCheck'],
                        toID = dataExport['toID'],
                        sumcompound = dataExport['compoundSum'],
                        avgcompound = average
                    )




class nytimesUpdater(abstractBaseUpdater):
    def __init__(self):
        super().__init__(crawlers.nyTimesCrawler(), 'nytimes', 'USA')

class yonhapUpdater(abstractBaseUpdater):
    def __init__(self):
        super().__init__(crawlers.yonhapCrawler(), 'yonhap', 'KOR')

class ecnsUpdater(abstractBaseUpdater):
    def __init__(self):
        super().__init__(crawlers.ecnsCrawler(), 'ecns', 'CHN')

class japantimesUpdater(abstractBaseUpdater):
    def __init__(self):
        super().__init__(crawlers.japantimesCrawler(), 'japantimes', 'JPN')
"""
class rodongUpdater(abstractBaseUpdater):
    def __init__(self):
        super().__init__(crawlers.rodongCrawler(), 'rodong', 'PRK')
"""
