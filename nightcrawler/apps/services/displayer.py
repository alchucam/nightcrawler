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
        today = timezone.now()
        yesterday = today - timedelta(1)
        queryset = dict()
        publisher_list = ['nytimes', 'yonhap', 'ecns','japantimes']
        for publisher in publisher_list:
            query = get_list_or_404(newsData.objects.order_by('id'), publisher=publisher, date=yesterday)[-1]
            # if newsData.objects.filter(publisher=publisher, date=today).exists():
            #     query = list(newsData.objects.filter(publisher=publisher, date=today))[-1]
            # else:
            #     query = list(newsData.objects.filter(publisher=publisher, date=yesterday))[-1]
            #try:
                #query = get_list(newsData.objects.order_by('id'), publisher=publisher, date=today)[-1]

            #query = list(newsData.objects.filter(publisher=publisher, date=yesterday))[-1]

            #except newsData.DoesNotExist:
            #    query = get_list(newsData.objects.order_by('id'), publisher=publisher, date=yesterday)[-1]
            #     query = newsData.objects.filter(publisher=publisher, date=yesterday).order_by('id').reverse()[0]

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

    #displayer methods for search
    def search_find_avgcompound(self, keyword, fSearch):
        epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
        analysis_processed = list()
        ratio_processed = list()
        for i in range(0, 7):
            analysis_innerlist = list()
            ratio_innerlist = list()
            avgcompound = 0
            sumcompound = 0
            count = 0 #number of query; same as to_num in collectedData
            day = int(((timezone.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0) - timedelta(days=i))-epoch).total_seconds()*1000.0)
            try:
                queryset = newsData.objects.filter(publisher=fSearch, date=timezone.now()-timedelta(i), freqList__contains=keyword)
                total_num = newsData.objects.filter(publisher=fSearch, date=timezone.now()-timedelta(i)).count()


                #for sentiment analysis highcharts
                for query in queryset:
                    sumcompound += query.compound
                    count += 1
                if count is not 0:
                    avgcompound = sumcompound/count
                    analysis_innerlist.extend([day, float(round(avgcompound, 3))])
                else:
                    analysis_innerlist.extend([day, 0])
                analysis_processed.append(analysis_innerlist)

                #for ratio highcharts
                if total_num is 0:
                    ratio_innerlist.extend([day, 0])
                else:
                    ratio_innerlist.extend([day,round((count/total_num),3)])
                ratio_processed.append(ratio_innerlist)

            except newsData.DoesNotExist:
                continue

        combined_processed = {'analysis':analysis_processed,'ratio':ratio_processed}
        return combined_processed


    def search_displayer(self, keyword):
        fromSearchList = ["nytimes", "ecns", "japantimes", "yonhap"]
        fromList = ["USA","CHN","JPN","KOR"]
        search_data = defaultdict(dict)
        for i in range(0, 4):
            search_data[fromList[i]] = self.search_find_avgcompound(keyword, fromSearchList[i])

        return search_data
