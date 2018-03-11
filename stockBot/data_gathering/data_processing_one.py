# this script will calculate the change in price from close to close for
#each stock for a period of one year (or more??) .
#then, in the next processing script, the crawling spiders will add html content to each stock by date
import pandas as pd
import os
import re
#from math import log
import numpy as np

def daily_change (x,y):
#    print x,y,x-y
#    print log(y/x)
    return np.log(y/x) #this is log base e will be used to calculate a stock's price change from close to close
                        #need numpy log for float64?? math.log did not work
datafolder='./daily_quotes_api'
filepaths=os.listdir(datafolder)
for f in filepaths:
    file_name=datafolder+'/'+f
    print f
    ticker_regex=re.compile('^(.*?)\_daily_data$')
    symbol=re.findall(ticker_regex,f)[0]
#open the stock data file
    FILE=pd.read_csv(file_name,nrows=260)     #start_date='2018-02-09    #end_date='2017-02-01'
    RES=pd.DataFrame()
    RES['date']=FILE.timestamp
    RES['ticker']=symbol
    tomorrow=FILE.close.shift(-1).fillna(0)
    today=FILE.close
    RES['daily_change']=daily_change(today,tomorrow)
    new_file_name=symbol+'_daily_changes'
    RES.to_csv(new_file_name)

# for a period of 1 year, calculate the change in stock price as log (day2close/day1close)

#make a csv file with date, stock symbole, price change columns
