# -*- coding: utf-8 -*-
from nightcrawler.apps.services.models import newsData, collectedData
from django.shortcuts import get_list_or_404
from django.utils import timezone

import pytz
from datetime import timedelta, datetime, time, date
from collections import defaultdict

#news_front_displayer: prepare data for news_front.html
#analysis_displayer and ratio_displayer: prepare data for analysis.html, esp. highcharts
class displayer(object):
    #latest
    def news_front_displayer(self):
        queryset = dict()
        publisher_list = ['nytimes', 'yonhap', 'ecns','japantimes']
        for publisher in publisher_list:
            query = get_list_or_404(newsData, publisher=publisher)[-1]
            queryset.update({publisher:{
                'publisher':query.publisher,
                'title':query.newsData_title,
                'url':query.url,
                'compound':query.compound,
                'freqList':query.freqList,
                'dateStr':query.dateStr,
                'date':query.date,
                'isArticle':query.isArticle}})
        return queryset

    #sub-method for analysis_displayer
    def list_creator(self, fromCountry, toCountry):
        epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
        #utc-awrare milliseconds
        weeklist = list()
        processed = list()

        #get milliseconds format for javascript
        for i in range(0, 7): #going from today -> last 7 days
            innerlist = list()
            day = int(((timezone.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0) - timedelta(days=i))-epoch).total_seconds()*1000.0)
            try:
                query = collectedData.objects.get(fromCountry=fromCountry, toCountry=toCountry, date=timezone.now() - timedelta(i))
                if query.avgcompound is None:
                    innerlist.extend([day, 'null'])
                else:
                    innerlist.extend([day, float(query.avgcompound)])
                processed.append(innerlist)
            except collectedData.DoesNotExist: #if no data, skip the day
                continue
        return processed

    #prepares all the necessary data for highcharts in the template
    def analysis_displayer(self):

        fromList = ["USA","CHN","JPN","KOR"]
        toList = ["USA","CHN","JPN","KOR","PRK"]


        template_data = defaultdict(dict)
        for fCon in fromList:
            for tCon in toList:
                template_data[fCon][tCon] = self.list_creator(fCon, tCon)
        return template_data

    #sub-method for ratio_displayer
    def ratio_creator(self, fromCountry, toCountry):
        epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
        #utc-awrare milliseconds
        weeklist = list()
        processed = list()
        #get milliseconds format for javascript
        for i in range(0, 7): #going from today -> last 7 days
            innerlist = list()
            day = int(((timezone.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0) - timedelta(days=i))-epoch).total_seconds()*1000.0)
            try:
                query = collectedData.objects.get(fromCountry=fromCountry, toCountry=toCountry, date=timezone.now()-timedelta(i))
                if query.total_num is 0:
                    innerlist.extend([day, 0])
                else:
                    innerlist.extend([day,round((query.to_num/query.total_num),3)])
                processed.append(innerlist)
            except collectedData.DoesNotExist: #no data, skip the day
                continue
        return processed

    #prepares all the necessary data for highcharts-area(ratio) in the template
    def ratio_displayer(self):

        fromList = ["USA","CHN","JPN","KOR"]
        toList = ["USA","CHN","JPN","KOR","PRK"]

        ratio_data = defaultdict(dict)
        for fCon in fromList:
            for tCon in toList:
                ratio_data[fCon][tCon] = self.ratio_creator(fCon, tCon)

        return ratio_data
