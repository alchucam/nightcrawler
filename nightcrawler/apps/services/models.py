# -*- coding: utf-8 -*-

from django.db import models
from datetime import timedelta, datetime, time, date
from django.utils import timezone

class newsData(models.Model):
    publisher = models.CharField(max_length=50)
    title = models.CharField(max_length=200, null=True, blank=True, unique=False)
    url = models.URLField(max_length=2000, null=True, blank=True)
    dateStr = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateField(default=timezone.now, db_index=True, null=True, blank=True)
    compound = models.DecimalField(max_digits=4, decimal_places=3,null=True, blank=True)
    freqList = models.CharField(max_length=1000, null=True, blank=True)
    isArticle = models.BooleanField() #true if the article is an actual article; false if noncontent(i.e. photo only) article.

    class Meta:
        verbose_name_plural = 'News Data'

    def __str__(self):
        return self.publisher + " " + self.dateStr + " " + str(self.newsData_id) + " " + self.title

    @property
    def newsData_id(self):
        return self.id
    @property
    def newsData_title(self):
        return self.title


class collectedData(models.Model):
    fromCountry = models.CharField(max_length=3)
    total_num = models.IntegerField()
    to_num = models.IntegerField()
    date = models.DateField(default=timezone.now, db_index=True, null=True, blank=True)
    toCountry = models.CharField(max_length=3)
    toCheck = models.BooleanField(default=False)
    toID = models.CharField(max_length=2000)
    sumcompound = models.DecimalField(max_digits=5, decimal_places=3,null=True, blank=True)
    avgcompound = models.DecimalField(max_digits=5, decimal_places=3,null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Collected Data'
    def __str__(self):
        return str(self.date) + " from " + self.fromCountry + " to " + self.toCountry + " exists: " + str(self.toCheck)
