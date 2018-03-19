# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
import json
from django.utils import timezone

# Create your models here.

class stockSearch(models.Model):
    unique_id=models.CharField(max_length=100,null=True)
    headline=models.CharField(max_length=255)
    postDate=models.DateTimeField()
    dateCrawled=models.DateTimeField(auto_now_add=True)
    link=models.URLField()
    articleHTML=models.TextField(default="html should be here")
    stockTicker=models.TextField(max_length=5, default="XXXX")
# This is for basic and custom serialisation to return it to client as a JSON.
    @property
    def to_dict(self):
        data = {
            'headline': json.loads(self.headline),
            'postDate': self.postDate,
            'link':self.link,
            'article_html':self.articleHTML
        }
        return data

    def __str__(self):
        return self.unique_id


class cnbcStockSearch(models.Model):
    unique_id=models.CharField(max_length=100,null=True)
    headline=models.CharField(max_length=255)
    postDate=models.DateTimeField()
    dateCrawled=models.DateTimeField(auto_now_add=True)
    link=models.URLField()
    articleHTML=models.TextField(default="html should be here")
    stockTicker=models.TextField(max_length=5, default="XXXX")
    sentiment=models.TextField(max_length=20,default="unknown")
# This is for basic and custom serialisation to return it to client as a JSON.
    @property
    def to_dict(self):
        data = {
            'headline': json.loads(self.headline),
            'postDate': self.postDate,
            'link':self.link,
            'article_html':self.articleHTML
        }
        return data

    def __str__(self):
        return self.unique_id

class bloombergStockSearch(models.Model):
    unique_id=models.CharField(max_length=100,null=True)
    headline=models.CharField(max_length=255)
    postDate=models.DateTimeField()
    dateCrawled=models.DateTimeField(auto_now_add=True)
    link=models.URLField()
    articleHTML=models.TextField(default="html should be here")
    stockTicker=models.TextField(max_length=5, default="XXXX")
    sentiment=models.TextField(max_length=20,default="unknown")
# This is for basic and custom serialisation to return it to client as a JSON.
    @property
    def to_dict(self):
        data = {
            'headline': json.loads(self.headline),
            'postDate': self.postDate,
            'link':self.link,
            'article_html':self.articleHTML
        }
        return data

    def __str__(self):
        return self.unique_id

class all_stock_names(models.Model):
    name=models.CharField(max_length=40, null=False)
    symbol=models.CharField(max_length=5,null=False)
    sector=models.CharField(max_length=30,null=True)
    industry=models.CharField(max_length=50,null=True)
    marketCap=models.BigIntegerField()
    def __str__(self):
        return self.name +'  |  '+self.symbol

#class stock_daily(models.Model):
#    trade_date=models.DateTimeField
#    symbol=models.textField(default="Ticker symbol is missing")
#    open_price=models.DecimalField(max_digits=10, decimal_places=4)
#    high_price=models.DecimalField(max_digits=10, decimal_places=4)
#    low_price=models.DecimalField(max_digits=10, decimal_places=4)
#    close_price=models.DecimalField(max_digits=10, decimal_places=4)
#    volume=models.PositiveIntegerField()
