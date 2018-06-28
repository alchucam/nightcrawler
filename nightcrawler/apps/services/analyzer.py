# -*- coding: utf-8 -*-

#sentiment analysis
#opinion mining

import nltk
import json
from nltk import ngrams
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nightcrawler.apps.services.models import newsData
from django.utils import timezone

nltk.data.path.append('./nltk_data/')

#portion 1: sentiment analysis
#portion 2: top 10 frequent words
#portion 3: analyze for collectedData model
class analyzer(object):
    #portion 1:

    #remove stop words or short words from the text
    def remove_stop_1gram(self, text, stop_words):
        tokenizer = RegexpTokenizer(r'\w+')

        tokens = []
        for line in  nltk.sent_tokenize(text):
            toks = tokenizer.tokenize(line)
            toks = [t for t in toks if t.lower() not in stop_words] #if a word is stop_words, not considered a word
            toks = [t for t in toks if len(t) >= 3] #if a word is less than 3, not considered a word
            tokens.extend(toks)
        return tokens

    #obtain frequent bigram words list, and remove bigrams stop words in the frequent list
    def remove_stop_2grams(self, text, stop_words):
        tokens = []
        two_grams = ngrams(text.split(), 2)
        two_freqs = nltk.FreqDist(two_grams)

        for two in two_freqs.most_common(30):
            if two[0][0] not in stop_words and two[0][1] not in stop_words:
                tokens.append(two)
        return tokens

    #obtain the top 15 frequent bigram words
    def take_bigram(self, text, stop_words):
        finder = BigramCollocationFinder.from_words(text)
        return finder.nbest(BigramAssocMeasures.likelihood_ratio, 15)

    #combine any two 1gram words into one 2gram words if they have same number of frequency,
    #then return top 10 words.
    def bigram_combine(self, bigram, tokens_freq):
        processed_tokens = list()
        count = 10 #number we want to show on the html
        temp = tuple() #other part of bi that we need to look for
        temp_tok = tuple() #temproary container for tok
        temp_num = int()
        first_check = False
        for bi in bigram:
            for tok in tokens_freq.most_common(18):
                if count > 0:
                    if temp is tok[0]: #found the pair match
                        if temp_num is tok[1]: #found the match and same frequency
                            if first_check:
                                processed_tokens.append(tuple([temp_tok+' '+tok[0],tok[1]]))
                            else:
                                processed_tokens.append(tuple([tok[0]+' '+temp_tok,tok[1]]))
                                #rest
                            count -= 1
                        else: #found the match but different frequency. considered fail
                            processed_tokens.append(tuple([temp_tok,temp_num]))
                            processed_tokens.append(tok)
                            count -= 2
                        #reset
                        temp = ()
                        temp_tok = ()
                        temp_num = 0
                        first_check = False

                    if tok[0] in bi: #found single match
                        temp_tok = tok[0]
                        temp_num = tok[1]
                        if tok[0] is bi[0]: #matched to first element
                            temp = bi[1]
                            first_check = True
                        else: #matched to second element
                            temp = bi[0]
                    else: #no match at all
                        processed_tokens.append(tok)
                        count -= 1
        return processed_tokens[:10] #ensure only top 10 is saved


    #method for analysis of compound calculation
    #returns the average of all compound
    def senti_Analysis(self, text):
        sia = SIA()
        results = []
        compoundAvg = 0
        for line in nltk.sent_tokenize(text):
            pol_score = sia.polarity_scores(line)
            pol_score['headline'] = line
            results.append(pol_score)
        for result in results:
            compoundAvg += result['compound']
        if not len(results) is 0:
            compoundAvg /= len(results)
        return compoundAvg


    #return compound score/sentiment score
    #calculate words freq
    #returns top 15 frequent numbers of stopwords removed, bigram combined tokens
    def word_freq(self, text):
        stop_words = stopwords.words('english')
        new_stop_words = ['Mr.','Mrs.','Ms.','mr','mrs','ms','said','say','would',]
        stop_words += new_stop_words

        one_tokens = self.remove_stop_1gram(text, stop_words)
        bigram = self.take_bigram(one_tokens, stop_words)
        one_tokens_freq = nltk.FreqDist(one_tokens)
        proccessed_tokens = self.bigram_combine(bigram, one_tokens_freq)

        return json.dumps(proccessed_tokens, ensure_ascii=False)


#actual keywords to be used as a keyword search in toRelationship method
    def country_expand(self, country):
        if country is 'USA':
            return ('United States', 'America', 'American')
        elif country is 'CHN':
            return ('China', 'Chinese')
        elif country is 'KOR':
            return ('South Korea', 'South Korean', 'S. Korea', 'S. Korean')
        elif country is 'PRK':
            return ('North Korea', 'North Korean', 'N. Korea', 'N. Korean', 'DPRK', 'Kim')
        elif country is 'JPN':
            return ('Japan', 'Japanese')
        elif country is 'TWN':
            return ('Taiwan', 'Taiwanese')
        else:
            return 'Country Input Error' #safetybox


#organize and export data regarding whether articles mentioned the target ('to') countries keywords such as ("South Korea")
#If so, obtain the ID of articles, update the number of such articles, and sum of compound (Sentiment scores) of such articles.
#dataExport will be sent to stored in collectedData.
#data: newsData
#country: target country
    def toRelationship(self, datum, country):
        dataExport = dict() #export to collectedData
        IDlist = str() #list of ID mentioning the target countries.
        toCheck = False #True if there's any articles mentioning the target countries at all.
        to_num = 0 #number of articles mentioning the target countries keywords.
        #to split a bigram word such as 'South Korea', and look if freqList mentions both/each words of bigram.
        splitOneCheck = False
        splitTwoCheck = False
        full_country = self.country_expand(country)

        compoundSum = 0

        for a_country in full_country: #a_country: a name of the country in the lists; also it acts as a keyword to be searched in the articles.

            if ' ' in a_country: #if it is a splitable word = bigram
                one, two = a_country.split()
                for freq in json.loads(datum.freqList, encoding='utf-8'):
                    if one in freq[0]:
                        splitOneCheck = True
                    if two in freq[0]:
                        splitTwoCheck = True
                    if splitOneCheck and splitTwoCheck:
                        toCheck = True
                        break
            else:
                if a_country in datum.title or a_country in datum.freqList: #check both title or top 10 frequent words
                    toCheck = True
                    break
        if toCheck: #if keyword found
            IDlist = str(datum.newsData_id)
            to_num = 1
            if datum.compound is not None:
                compoundSum += datum.compound
            else:
                compoundSum += 0

        dataExport.update({
            'toCheck':toCheck,
            'toID':IDlist,
            'to_num':to_num,
            'compoundSum':compoundSum})

        return dataExport

    #obtain total number of articles for ratio analysis
    def total_articles(self, publisher):
        num = 0

        #for publisher in publishers:
        articles = newsData.objects.filter(publisher=publisher, date=timezone.now())
        for article in articles:
            num += 1
        return num
