# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.urls import reverse
from uuid import uuid4
import requests
import json
#from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View  #class based views inherit from View
from django.views.generic.base import TemplateView #needed for class-view templates
from scrapyd_api import ScrapydAPI
#from django.utils import URLUtil
from .models import *
from .forms import *
from scrapy.utils.project import get_project_settings
from dal import autocomplete
import time

from .sentiment_script_custom import clean_article
from .sentiment_script_custom import sentiment_analysis
# Create your views here.

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')  #how do I make api calls to here?
#in shell go to stockCrawl/stockBot/stockBot and type scrapyd to launch twisted to port 6800
#latest version of scrapyd-client pip install git+https://github.com/scrapy/scrapyd-client

def landing(request):
    dow_url='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=DJI&outputsize=compact&apikey=TJ86LY8QFCFMQ44Z&datatype=json&interval=15min'
    sp500_url='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=INX&outputsize=compact&apikey=TJ86LY8QFCFMQ44Z&datatype=json&interval=15min'
    nasdaq_url='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IXIC&outputsize=compact&apikey=TJ86LY8QFCFMQ44Z&datatype=json&interval=15min'
    test="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&outputsize=compact&apikey=TJ86LY8QFCFMQ44Z&datatype=json&interval=15min"

    form=searchStockForm
    context={'form':form}

    return render(request,'stockSite/landing.html',context)

#api for stock data: https://www.alphavantage.co/documentation/
#url='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAYY&symbol='+stock+'&outputsize=compact&apikey=TJ86LY8QFCFMQ44Z&datatype=json'

def crawlbb(request):  #crawls a page of bloomber news
    stock=request.POST['stock']
    symbol=request.POST['symbol']
    print "bloomberg crawl beginning for: ",stock,symbol
    if not stock:
        return JsonResponse({'error': 'Missing  args: stock'})

    #domain = urlparse(url).netloc # parse the url and extract the domain
    task_id = str(uuid4()) # create a unique ID.
    # This is the custom settings for scrapy spider.
    settings = {
        'job_id': task_id, # unique ID for each record for DB
        'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }

    # Here we schedule a new crawling task from scrapyd.
    # Notice that settings is a special argument name.
    # But we can pass other arguments, though.
    # This returns a ID which belongs and will be belong to this task
    # We are goint to use that to check task's status.
    '''These are functions from the srcapyd API. they seem to not invoke the stockbot project, but rather the default project'''
        #settings = get_project_settings()
        #project_list=requests.get('http://localhost:6800/listspiders.json?project=default')
        #print "project list: ",project_list.json()
        #task=requests.post('http://localhost:6800/schedule.json -d project=default -d spider=cnbcSpider_web')
        #print "statusQ: ",statusQ.json()
        #return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })
    task = scrapyd.schedule('stockBot', 'bbSpider',settings=settings, symbol=symbol,stock=stock, task_id=task_id)
    status = None

    while (status != 'finished'):  #trigger used to emulate do...while loop
        print status
        if status == 'finished':
            print "status of bbcrawl: finished"
        else:
            status = scrapyd.job_status('stockBot', task)
            print "still waiting for bb crawl to finish"
            print status
            time.sleep(3)
    items = bloombergStockSearch.objects.filter(unique_id=task_id)
    data=serializers.serialize('json',items)
    return JsonResponse(data,safe=False)

def crawlcnbc(request):  #crawls a page of bloomber news
    stock=request.POST['stock']
    symbol=request.POST['symbol']
    print "cnbc crawl beginning for: ",stock,symbol
    if not stock:
        return JsonResponse({'error': 'Missing  args: stock'})
    task_id = str(uuid4()) # create a unique ID.
    settings = {
        'job_id': task_id, # unique ID for each record for DB
        'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }

    task = scrapyd.schedule('stockBot', 'cnbcSpiderWeb',settings=settings, symbol=symbol,stock=stock, task_id=task_id)
    status = None

    while (status != 'finished'):  #trigger used to emulate do...while loop
        print status
        if status == 'finished':
            print "status of cnbc crawl: finished"
        else:
            status = scrapyd.job_status('stockBot', task)
            print "still waiting for cnbc crawl to finish"
            print status
            time.sleep(3)
    items = cnbcStockSearch.objects.filter(unique_id=task_id)
    data=serializers.serialize('json',items)
    return JsonResponse(data,safe=False)


class stockSearchAutocomplete(autocomplete.Select2QuerySetView,TemplateView):
    #template_name='stockSite/landing.html'
    model=all_stock_names
    form_class=searchStockForm
    def get_queryset(self):
        qs=all_stock_names.objects.all()
        if self.q:    # responds to format http://localhost:5000/search/?q=apple
            qs=qs.filter(name__istartswith=self.q).order_by('-marketCap')
            print type(qs)
        return qs
    def post(self,request):
        print "autocomplete View POST invoked",request.POST['name']
        stockID=request.POST['name']
        stock=all_stock_names.objects.get(id=stockID)
        print stock.name
        context={'stock':stock.name, 'symbol':stock.symbol}
        return render(request,'stockSite/crawl.html',context)

def customText(request):
    print "custom text entered"
    #print request.POST['customText']
    customText=request.POST['customText']
    clean_text=clean_article(customText)
    #print article_html has trouble printing ascii character
    article_in_array=[clean_text]
    sentiment={'sentiment':sentiment_analysis(article_in_array)}
    result=json.dumps(sentiment)
    #sentiment="test sentiment result"
    return JsonResponse(result,safe=False)
'''
def index(request):
    return render(request,'stockSite/index.html')

def indexcrawl(request):
    # Post requests are for new crawling tasks
    if request.method == 'POST':

        stock = request.POST['stock'].strip().lower() # take url comes from client. (From an input may be?)

        if not stock:
            return JsonResponse({'error': 'Missing  args'})

        #if not is_valid_url(url):
        #    return JsonResponse({'error': 'URL is invalid'})

        #domain = urlparse(url).netloc # parse the url and extract the domain
        unique_id = str(uuid4()) # create a unique ID.

        # This is the custom settings for scrapy spider.
        # We can send anything we want to use it inside spiders and pipelines.
        # I mean, anything
        settings = {
            'unique_id': unique_id, # unique ID for each record for DB
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        # Here we schedule a new crawling task from scrapyd.
        # Notice that settings is a special argument name.
        # But we can pass other arguments, though.
        # This returns a ID which belongs and will be belong to this task
        # We are goint to use that to check task's status.
        #settings = get_project_settings()

        print "starting bb spider in indexcrawl for: ", stock
        symbol="TEST"
        task = scrapyd.schedule('stockBot', 'bbSpider', symbol=symbol,stock=stock)

        #return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })
        return redirect('/')
    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':
        # We were passed these from past request above. Remember ?
        # They were trying to survive in client side.
        # Now they are here again, thankfully. <3
        # We passed them back to here to check the status of crawling
        # And if crawling is completed, we respond back with a crawled data.
        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)

        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})

        # Here we check status of crawling that just started a few seconds ago.
        # If it is finished, we can query from database and get results
        # If it is not finished we can return active status
        # Possible results are -> pending, running, finished
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # this is the unique_id that we created even before crawling started.
                item = ScrapyItem.objects.get(unique_id=unique_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})
'''
