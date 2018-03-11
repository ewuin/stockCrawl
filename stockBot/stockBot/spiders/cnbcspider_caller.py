
#50 most popular stocks from this site
#https://hedgemind.com/stock-ideas/50-most-popular-stocks-among-hedge-funds
# AAPL omitted from this array, this data was successfully gathered as a test
#nxpi omitted because serach term nxp semiconductors didn't yield results on manual search at cnbc.com
#IAC, and jd .com also omited

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
    print stock
#    print stock['name']
#    print stock['symbol']
print "testing curl"
