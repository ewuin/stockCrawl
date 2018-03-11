import os
import requests
import time

API_KEY='TJ86LY8QFCFMQ44Z'
stock_array=[
        'FB','BABA','AMZN','MSFT','BAC','GOOG','V',
        'AABA','CHTR','C','AAPL','CRM','NFLX','AGN',
        'TWX','EXPE','MA','PYPL','AVGO','MON','NXPI',
        'DAL','JD','JPM','TMUS','ADBE','ATVI','DXC','STZ',
        'PCLN','MGM','NVDA','SHPG','ADSK','EA','WFC',
        'ALXN','DVMT','MU','NOW','ZAYO','AET','ALLY',
        'ANTM','CELG','CLVS','INCY','UNH','IAC','PE'
        ]

for stock in stock_array:
    url='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stock+'&outputsize=full&apikey=TJ86LY8QFCFMQ44Z&datatype=csv'
    file_name=stock+"_daily_data"
    response = requests.get(url)
    with open(os.path.join(".", file_name), 'wb') as f:
        f.write(response.content)
    time.sleep(1)
#website asks 1 call per second

#50 most popular stocks from this site
#https://hedgemind.com/stock-ideas/50-most-popular-stocks-among-hedge-funds

#FB,BABA,AMZN,MSFT,BAC,GOOG,V,AABA,CHTR,C,AAPL,CRM,NFLX,AGN,TWX,EXPE,MA,PYPL,AVGO,MON,NXPI,DAL,JD,JPM,TMUS,ADBE,ATVI,DXC,STZ,PCLN,MGM,NVDA,SHPG,ADSK,EA,WFC,ALXN,DVMT,MU,NOW,ZAYO,AET,ALLY,ANTM,CELG,CLVS,INCY,UNH,IAC,PE
