import os
import sys
import django
sys.path.append(os.path.dirname(os.path.abspath('.')))
DJANGO_PROJECT_PATH='C:/Users/Owner/Documents/CodingDojo/stock_project/stocks_3/stockCrawl'
DJANGO_SETTINGS_MODULE='stockCrawl.settings'
sys.path.insert(0,DJANGO_PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE']=DJANGO_SETTINGS_MODULE
django.setup()
from apps.stockSite.models import stockSearch, cnbcStockSearch, bloombergStockSearch
## all these lines above needed to access database
#other needed libraries below
import re
import pandas as pd
from django_pandas.io import read_frame
import numpy
datafolder='./daily_changes/'
filepaths=os.listdir(datafolder)
### test code ###
#articles=stockSearch.objects.all()
#print "articles amount is : "
#print len(articles)

    #stock_name = "UNH"
def add_articles(stock_name):  # feed in the ticker symbol such as 'AAPL'
    # find stock data in sqlite db
    stock_articles=cnbcStockSearch.objects.filter(stockTicker=stock_name).values('headline','postDate','articleHTML')#.dates('postDate','day')
    # combine all html from each date into one row
    stock_frame=read_frame(stock_articles) #converts orm query to pandas dataframe
            #test=stock_frame.postDate.map(lambda x:x.date()) this works to return just the date
    articles_by_date=stock_frame.groupby([stock_frame.postDate.map(lambda x:x.date())])['headline','articleHTML'].sum()  #this method returns a data frame
    articles_by_date.reset_index(inplace=True)
            #articles_by_date.agg({'headline':'sum','articleHTML':'sum'}) # this will return a group, which wont convert to csv
            #print articles_by_date.head()
    # append stock data for that date from _daily_changes file
    file_name=datafolder+stock_name+"_daily_changes" #file with daily log(close/previous_day_close) ratios
    price_data=pd.read_csv(file_name)     #start_date='2018-02-09    #end_date='2017-02-01'
    price_data['date']=price_data['date'].apply(pd.to_datetime)   #date column was read as strings
    articles_by_date['postDate']=articles_by_date['postDate'].apply(pd.to_datetime)
            #print type(articles_by_date.postDate[0])
            #print type(price_data.date[0])
    final_data=pd.merge(articles_by_date,price_data,how="inner",left_on='postDate',right_on="date")

    #write to csv
        #print final_data.head()
    new_file_name=stock_name+"_articles_and_prices.csv"
    final_data.to_csv(new_file_name,encoding='utf-8')  #second argument necessary to avoid error: ascii codec can't encode character ... ordinal not in range (128)

stock_array=[
        {'name':'facebook','symbol':'FB'},
        {'name':'alibaba', 'symbol':'BABA'},
        {'name':'amazon', 'symbol':'AMZN'},
        {'name':'microsoft', 'symbol':'MSFT'},
        {'name':'bank of america', 'symbol':'BAC'},
        {'name':'google', 'symbol':'GOOG'},
        {'name':'visa', 'symbol':'V'},
        {'name':'altaba', 'symbol':'AABA'},
        {'name':'charter communications', 'symbol':'CHTR'},
        {'name':'citigroup', 'symbol':'C'},
        {'name':'salesforce', 'symbol':'CRM'},
        {'name':'netflix', 'symbol':'NFLX'},
        {'name':'allergan', 'symbol':'AGN'},
        {'name':'time warner', 'symbol':'TWX'},
        {'name':'expedia', 'symbol':'EXPE'},
        {'name':'mastercard', 'symbol':'MA'},
        {'name':'paypal', 'symbol':'PYPL'},
        {'name':'broadcom', 'symbol':'AVGO'},
        {'name':'monsanto', 'symbol':'MON'},
        {'name':'delta airlines', 'symbol':'DAL'},
        {'name':'jp morgan', 'symbol':'JPM'},
        {'name':'t-mobile', 'symbol':'TMUS'},
        {'name':'adobe', 'symbol':'ADBE'},
        {'name':'activision blizzard', 'symbol':'ATVI'},
        {'name':'dxc technology', 'symbol':'DXC'},
        {'name':'constellation brands', 'symbol':'STZ'},
        {'name':'priceline', 'symbol':'PCLN'},
        {'name':'mgm resorts', 'symbol':'MGM'},
        {'name':'nvidia', 'symbol':'NVDA'},
        {'name':'shire', 'symbol':'SHPG'},
        {'name':'autodesk', 'symbol':'ADSK'},
        {'name':'electronic arts', 'symbol':'EA'},
        {'name':'wells fargo', 'symbol':'WFC'},
        {'name':'alexion', 'symbol':'ALXN'},
        {'name':'dell', 'symbol':'DVMT'},
        {'name':'micron', 'symbol':'MU'},
        {'name':'servicenow', 'symbol':'NOW'},
        {'name':'zayo', 'symbol':'ZAYO'},
        {'name':'aetna', 'symbol':'AET'},
        {'name':'ally financial', 'symbol':'ALLY'},
        {'name':'anthem', 'symbol':'ANTM'},
        {'name':'celgene', 'symbol':'CELG'},
        {'name':'clovis', 'symbol':'CLVS'},
        {'name':'incyte', 'symbol':'INCY'},
        {'name':'unitedhealth', 'symbol':'UNH'},
        {'name':'parsley energy', 'symbol':'PE'}
        ]

for stock in stock_array:
    print stock['name']
    add_articles(stock['symbol'])


#print len(FILE)
#print FILE.head()
#RES=pd.DataFrame()
