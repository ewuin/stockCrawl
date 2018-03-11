import os
import sys
import django
sys.path.append(os.path.dirname(os.path.abspath('.')))
DJANGO_PROJECT_PATH='C:/Users/Owner/Documents/CodingDojo/stock_project/stocks_3/stockCrawl'
DJANGO_SETTINGS_MODULE='stockCrawl.settings'
sys.path.insert(0,DJANGO_PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE']=DJANGO_SETTINGS_MODULE
django.setup()
from apps.stockSite.models import all_stock_names
## all these lines above needed to access database
#other needed libraries below
import re
import pandas as pd
import numpy as np
from django_pandas.io import read_frame

file1="companylist.csv"    #these two files should have all security names traded on NASDAQ and NYSE
file2="companylist2.csv"    #file1 has stocks on the NYSE, file2 has stocks on the nasdaq
file_name=file1

#get rid of commas and periods
exclude=[".",","]
#clean company names of "inc, ltd, corp, corporation, l.p. plc
corp_remover=re.compile(r'^corp(\.)?$',re.IGNORECASE)
corp2_remover=re.compile(r'^corporation$',re.IGNORECASE)
inc_remover=re.compile(r'^inc(\.)?$',re.IGNORECASE)
ltd_remover=re.compile(r'^ltd(\.)?$',re.IGNORECASE)
lp_remover=re.compile(r'^l(\.)?p(\.)?$',re.IGNORECASE)
plc_remover=re.compile(r'^p(\.)?l(\.)?c(\.)?$',re.IGNORECASE)
excludeMoney=["$","B","M","m","b"]  #used to conver market cap to long type int


def clean_names(stockName):
    nameList=stockName.split()
    cleaner_name=""
    for word in nameList:
        if not (re.match(inc_remover,word) or re.match(corp_remover,word) or re.match(corp2_remover,word) or re.match(ltd_remover,word) or re.match(lp_remover,word) or re.match(plc_remover,word)):  #for some reason only choosing the words that didnt match the regex removed the unwanted word better
            cleaner_name=cleaner_name+word+" "
    clean_name  = "".join(ch for ch in cleaner_name if ch not in exclude)
    return clean_name

def convert_MktCap(mktCapString):
    if (mktCapString[-1]=="M" or mktCapString[-1]=="m"):
        multiplier=1000000   #million
    elif (mktCapString[-1]=="B" or  mktCapString[-1]=="b"):
        multiplier=1000000000 #billion
    else:
        multiplier=1
    clean_string="".join(ch for ch in mktCapString if ch not in excludeMoney)
    mktCap=long(float(clean_string) * multiplier)
    return mktCap

def convert_MktCap_two(mktCapFloat):
    return long(mktCapFloat)


#read file in, save into pd DataFrame  #get rid of rows with sector ="NaN", and market caps na
unclean_data=pd.read_csv(file_name)
unclean_data=unclean_data.dropna(subset=["Sector","MarketCap"])
#unclean_data=unclean_data[unclean_data.MarketCap>0] #for file2
print len(unclean_data)
#clean names of unwanted chars and words
unclean_data['Name']=unclean_data['Name'].apply(clean_names)
#convert market cap to big int type
unclean_data['MarketCap']=unclean_data['MarketCap'].apply(convert_MktCap) #for file1
#unclean_data['MarketCap']=unclean_data['MarketCap'].apply(convert_MktCap_two)  #for file 2 #for file 2
#keep the columns: symbol, name, market cap, sector, and industry, dump all else
clean_data=unclean_data.to_dict(orient="records")
#write to database
for row in clean_data:
    all_stock_names.objects.create(name=row['Name'],symbol=row['Symbol'],sector=row['Sector'],industry=row['industry'], marketCap=row['MarketCap'])  #industry is lowercase in file 1, upper in 2
#print clean_data
#unclean_data.to_csv("test1.csv",encoding='utf-8')


#file1 had 2586 stocks on NASDAQ
#file2 had 1996 stocks on NYSE
