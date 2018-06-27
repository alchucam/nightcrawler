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
        for i in range(0, 7):
            weeklist.append(int(((timezone.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0) - timedelta(days=i))-epoch).total_seconds()*1000.0))
        queryset = collectedData.objects.filter(fromCountry=fromCountry, toCountry=toCountry, date__range=[timezone.now()-timedelta(days=7),timezone.now()]).order_by('-date')
        avgcompound_list = list()
        for query in queryset:
            if query.avgcompound is None:
                avgcompound_list.append('null')
            else:
                avgcompound_list.append(float(query.avgcompound))
        zipIt = zip(weeklist, avgcompound_list)
        for day, compound in zipIt:
            innerlist = list()
            innerlist.extend([day, compound])
            processed.append(innerlist)
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
        for i in range(0, 7):
            weeklist.append(int(((timezone.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0) - timedelta(days=i))-epoch).total_seconds()*1000.0))
        queryset = collectedData.objects.filter(fromCountry=fromCountry, toCountry=toCountry, date__range=[timezone.now()-timedelta(days=7),timezone.now()]).order_by('-date')
        ratiolist = list()
        for query in queryset:
            if query.total_num is not 0:
                ratiolist.append(round((query.to_num/query.total_num),3))
            else:
                ratiolist.append(0)
        zipIt = zip(weeklist, ratiolist)
        for day, compound in zipIt:
            innerlist = list()
            innerlist.extend([day, compound])
            processed.append(innerlist)
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
