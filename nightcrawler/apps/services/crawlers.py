# -*- coding: utf-8 -*-

from nightcrawler.apps.services.analyzer import *
from nightcrawler.apps.services.models import newsData, collectedData
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from bs4 import BeautifulSoup as BSoup
import datetime
import requests
import json

#parse to obtain data for newsData model
#parse happens in two parts. first to parse RSS(xml) or api(html). #second to parse each articles html
class abstractBaseCrawler(object):
    def __init__(self):
        self.headers = { 'user-agent': 'nightcrawler/1.0'}

    def xmlParse(self, xmlurl, publisher, keyword):
        r = requests.get(xmlurl)
        soup = BSoup(r.text, 'xml')

        dataExport = dict()
        compoundvalue = 0

        #parse xml
        for item in soup.find_all('item'):

            if publisher is 'yonhap':
                if '(Copyright)' in item.title.string:
                    continue
            title = item.title.string
            url = item.link.string

            if not newsData.objects.filter(title=title).exists(): #if it doesn't already exists.
                #publish date
                if publisher is 'yonhap':
                    time = item.pubDate.string[0:4] + '-' + item.pubDate.string[4:6] + '-' + item.pubDate.string[6:8]
                elif publisher is 'ecns':
                    time = item.pubDate.string[:10]
                elif publisher is 'japantimes':
                    time = datetime.datetime.strptime(item.pubDate.string[5:16], "%d %b %Y").strftime("%Y-%m-%d")

                #parse html
                r2 = requests.get(url)
                soup2 = BSoup(r2.text, 'html.parser')

                if soup2 is None:
                    continue #if url is not obtainable, skip to next one

                strContainer = "" #contents for analysis
                strContainer.encode(encoding='UTF-8',errors='strict')

                if publisher is 'yonhap' or publisher is 'ecns':
                    newsContent = soup2.find_all("div", class_= keyword)
                elif publisher is 'japantimes':
                    newsContentfind = soup2.find('div', id= keyword)
                    if newsContentfind is not None:
                        newsContent = newsContentfind.findAll('p')
                    else:
                        continue

                for content in newsContent:
                    strContainer = strContainer + " " + content.text

                if len(strContainer) < 20:
                    isArticle = False;
                else:
                    isArticle = True;

                analyzerObj = analyzer()
                compoundValue = analyzerObj.senti_Analysis(strContainer)
                wordFreq = analyzerObj.word_freq(strContainer)

                dataExport.update({title:{
                    'url': url,
                    'time': time,
                    'compound':compoundValue,
                    'word_freq':wordFreq,
                    'isArticle': isArticle}})

        return dataExport

class nyTimesCrawler(abstractBaseCrawler):
    def get_Contents(self):
        getURL = 'https://newsapi.org/v2/top-headlines?sources=the-new-york-times&apiKey={0}'.format(settings.NYTIMES_API_KEY)
        r = requests.get(getURL)
        json_data = r.json()
        dataExport = dict() #export crawled info out for data store
        compoundValue = 0 #sentiment score

        #parse json
        for article in json_data['articles']:
            title = article['title']
            url = article['url']
            time = article['publishedAt'][:10]

            #parse html
            r2 = requests.get(url)
            soup = BSoup(r2.text, 'html.parser')

            if soup is None:
                continue #if url is not obtainable, skip to next one

            pDict = dict() #p tag dictionary
            nonReg = False #check if the main body of articles has expected class name or non-expected class name (g-...)

            #parse p tag in html

            #one type of article. main body of articels has expected class name (i.e. css-1i0edl6 e2kc3sl0)
            for p in soup.find_all('p'):
                if p.get('class') is not None:
                    pName = " ".join(p.get('class'))
                    freq = pDict.get(pName)
                    if freq is not None:
                        freq += 1
                    else:
                        freq = 1
                    pDict.update({pName:freq})

            #different type of article. main body of articles has 'g-..'
            for p in pDict:
                if 'g-' in p:
                    nonReg = True
                    pDict = dict() #reset
                    for div in soup.find_all('div'):
                        if div.get('class') is not None:
                            divName = " ".join(div.get('class'))
                            freq = pDict.get(divName)
                            if freq is not None:
                                freq += 1
                            else:
                                freq = 1
                            pDict.update({divName:freq})

            #Figure out the most number of class name;
            #as I'm assuming the most nubmer of class name contain the article contents
            count = 0
            pMost = None
            for p in pDict.keys():
                if pDict[p] >= count:
                    count = pDict[p]
                    pMost = p

            #If there exsits g- class name, main articles are in div tag; otherwise it's in p tag.
            if not nonReg:
                newsContent = soup.find_all("p", class_ = pMost)
            else:
                newsContent = soup.find_all("div", class_= pMost)

            #if unable to retrieve the contents, skip the article [safebox]
            if newsContent is None:
                continue


            strContainer = "" #contents for analysis
            strContainer.encode(encoding='UTF-8',errors='strict')
            for content in newsContent[:]:
                if nonReg:
                    strContainer = strContainer + " " + content.p.text.replace('\n','')
                else:
                    strContainer = strContainer + " " + content.text

            #run analysis class methods to obtain sentiment score (compoundValue) and most frequent words (wordFreq)
            analyzerObj = analyzer()
            compoundValue = analyzerObj.senti_Analysis(strContainer)
            wordFreq = analyzerObj.word_freq(strContainer)

            if len(strContainer) < 20:
                isArticle = False;
            else:
                isArticle = True;

            #get one article
            dataExport.update({title:{
                'url': url,
                'time': time,
                'compound':compoundValue,
                'word_freq':wordFreq,
                'isArticle': isArticle}})
        return dataExport

class yonhapCrawler(abstractBaseCrawler):
    def get_Contents(self):
        return self.xmlParse('http://english.yonhapnews.co.kr/RSS/headline.xml','yonhap', 'article')

class ecnsCrawler(abstractBaseCrawler):
    def get_Contents(self):
        return self.xmlParse('http://www.ecns.cn/rss/rss.xml','ecns', 'content')

class japantimesCrawler(abstractBaseCrawler):
    def get_Contents(self):
        return self.xmlParse('https://www.japantimes.co.jp/feed/topstories/', 'japantimes', 'jtarticle')

""" for North Korean news website. Will turn it back on once they have better internet.
class rodongCrawler(abstractBaseCrawler):
    def get_Contents(self):
        link1 = 'http://www.rodong.rep.kp/en/'
        link2 = 'index.php?strPageID=SF01_01_02&iMenuID=2'
        r = requests.get(link1 + link2)
        soup = BSoup(r.text, 'html.parser')
        dataExport = dict()
        compoundValue = 0

        for articles in soup.find_all('div', class_= 'ListNewsLineContainer'):
            url = link1 + articles.a['href'][25:-2]
            title = articles.a.string
            time = articles.find('div',class_='ListNewsLineDate').string

            #parse news article
            r2 = requests.get(url)
            soup2 = BSoup(r2.text, 'html.parser')

            strContainer = "" #contents for analysis
            strContainer.encode(encoding='UTF-8',errors='strict')

            newsContent = soup2.find_all('p',class_="ArticleContent")
            for content in newsContent[:-1]:
                strContainer = strContainer + " " + content.text

            #run analysis class methods to obtain sentiment score (compoundValue) and most frequent words (wordFreq)
            analyzerObj = analyzer()
            compoundValue = analyzerObj.senti_Analysis(strContainer)
            wordFreq = analyzerObj.word_freq(strContainer)


            #get one article
            dataExport.update({title:{
                #'content':strContainer,
                'url': url,
                'time': time,
                'compound':compoundValue,
                'word_freq':wordFreq}})

        return dataExport
"""
