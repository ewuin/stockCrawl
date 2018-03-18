from scrapy.spiders import BaseSpider
from stockBot.items import cnbcStockbotItem
from selenium import webdriver
import datetime # must also import in models.py
import scrapy
import re
import uuid
from bs4 import BeautifulSoup as bsObj
import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())


class cnbcSpider(scrapy.Spider):
    name = "cnbcSpider"
    allowed_domains = ['cnbc.com']

    def __init__(self,*args,**kwargs):
        super(cnbcSpider, self).__init__(*args,**kwargs)
        self.stock=kwargs.get('name')
        self.symbol=kwargs.get('symbol')
        self.driver = webdriver.Firefox()

    def start_requests(self):
        print self.stock
        print self.symbol
        url='https://search.cnbc.com/rs/search/view.html?source=CNBC.com&categories=exclude&partnerId=2000&pubtime=0&keywords='
        url +=self.stock
        urls=[url]
        date_pattern=re.compile(r'(\d+)(.*)',re.UNICODE)
        end_date=datetime.datetime(2017,7,17)  #get news articles from Monday July 17 on
        current_date=datetime.datetime(2018,2,9) #start date for news is Feb. 9
              # switch to phantomJS or remote web driver later
            #self.driver.find_element_by_xpath('//*[@id="page"]/div/div[2]/div[1]/div[3]/dl/dt[1]/*').click() #need to click past twelve months option
        self.driver.get(url)
        try:
            self.driver.find_element_by_xpath('//*[@id="page"]/div/div[2]/div[1]/div[3]/dl/dt[1]/*').click()
        except:
            print "all results button already pushed, or not found"

        while current_date>=end_date:      #use firefox drive to click on next page link
            try:
                nextPage = self.driver.find_element_by_xpath('//*[@id="rightPagCol"]/a') #this is selenium technique to click "next page"
                current_date_html=self.driver.find_element_by_xpath('//*[@id="page"]/div/div[2]/div[2]/div/div[1]/div[10]/time').text
                #what to do if not enough elements on the page??
                match_date=date_pattern.findall(current_date_html)[0]
                match_date_groups=match_date[0]+match_date[1]
                if len(match_date[0])==1:   #dates are not zero-padded
                    formatted_date=match_date_groups[0:10]
                    current_date=datetime.datetime.strptime(formatted_date,'%d %b %Y')
                elif len(match_date[0])==2:
                    formatted_date=match_date_groups[0:11]
                    current_date=datetime.datetime.strptime(formatted_date,'%d %b %Y')

            #print current_date_before

        #    try:  old try
                nextPage.click()
                url=self.driver.current_url
                print "navigated to"+url
                urls.append(url)
                self.driver.get(url)
            except:
                print("next not clicked")
                break
        print urls
        for url in urls:
            time.sleep(1)
            yield scrapy.Request(url=url, callback=self.parse3)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'bb-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def parse2(self, response):
        for quote in response.css('div.search-result'):
            yield {
                'headline': quote.css('h1.search-result-story__headline::text').extract(),
                'post-date': quote.css('time.published-at').extract(),
                'link': quote.css('h1.search-result-story__headline').xpath('.//a').extract(),
                }


    def parse3(self, response):
        count = 0
        for quote in response.css('div.SearchResultCard'):
            unique_id=uuid.uuid4()
            d={
                'headline': quote.css('h3.title').xpath('.//a/text()').extract(),
                'post-date': quote.css('time').re(r'(\d+).*'),
                'link': quote.css('h3.title').xpath('.//a/@href').extract(),
                }


            print d['link']

            #try:
            #    video_link=quote.css('h3.title/span.icon-cnbc-video')
            #    print "SSSSSSSSS  This is a video link SSSSSSSSS"
            #except:
            #    "video link extraction error"

            formatted_date=d['post-date'][0]
            formatted_date=formatted_date[0:10]
            #print formatted_date
            formatted_date=datetime.datetime.fromtimestamp(int(formatted_date)).strftime('%Y-%m-%d %H:%M:%S')
            #print formatted_date
            #print type(x)
            #x=datetime.datetime.strptime(x,'%Y-%m-%dT%H:%M:%S')
            meta_dict={}
            meta_dict['unique_id']=unique_id
            meta_dict['headline']=d['headline']
            meta_dict['postDate']=formatted_date
            meta_dict['link']=d['link'][0]
            meta_dict['ticker']=self.symbol
            # meta dictionary passed to parse_article, which gets the desired html content of each article link
            count +=1
            print "This is article NUMBER: "+str(count)
            #except will try to fix article link
            try:
                yield scrapy.Request(url=d['link'][0],callback=self.parse_article,meta=meta_dict)
            except ValueError:
                prepended_link='https:'+str(meta_dict['link'])
                print "This link wont work: "+meta_dict['link']
                print "Trying this link: "+prepended_link
                meta_dict['link']=prepended_link
                yield scrapy.Request(url=prepended_link,callback=self.parse_article,meta=meta_dict)



    def parse_article(self,response):
        print "getting article page html"
        unique_id=response.meta['unique_id']
        headline=response.meta['headline'][0]
        postDate=response.meta['postDate']
        link=response.meta['link']
        tickerSymbol=response.meta['ticker']
        #article_type=response.meta['article_type']
        article_html=response.css('div.story').extract()


        if len(article_html)<1:
            article_html=bsObj(self.get_paragraphs(response),"html.parser").get_text()
            article_html=re.sub(r"^\s+", "", article_html, flags = re.MULTILINE)
            #stripped_content = ''.join(line.lstrip(' \t') for line in content.splitlines(True))
        else:
            article_html=bsObj(response.css('div.story').extract()[0], "html.parser").get_text().strip()
            article_html=re.sub(r"^\s+", " ", article_html, flags = re.MULTILINE)
            #article_html = ''.join(line.lstrip(' \t') for line in article_html.splitlines(True))
        #send this stock bot item to the database

        yield cnbcStockbotItem(unique_id=unique_id,headline=headline,postDate=postDate,link=link,articleHTML=article_html,stockTicker=tickerSymbol)


    def get_paragraphs(self,response_item):  #gets all <p> elements
        article_html=""
        divs=response_item.xpath('//div')
        for p in divs.xpath('.//p'):
            article_html+=p.extract()
        return article_html
## use cmd line prompt: scrapy crawl quotes -o quotes.json to store info as data
## if you reuse filename, it will make file unusable, because it will json the json and
# then append the new results

#alternatively use : scrapy crawl quotes -o quotes.jl
# to append lines of json

'''

stock_array=[
        #{'name':'facebook','symbol':'FB'},
        #{'name':'alibaba', 'symbol':'BABA'},
        #{'name':'amazon', 'symbol':'AMZN'}, redo amazon later, only have articles until sept.10 or so
        #{'name':'microsoft', 'symbol':'MSFT'},
        #{'name':'bank of america', 'symbol':'BAC'},
        #{'name':'google', 'symbol':'GOOG'},
        #{'name':'visa', 'symbol':'V'},
        #{'name':'altaba', 'symbol':'AABA'}, only got 2 articles
        #{'name':'charter communications', 'symbol':'CHTR'}, got about 10
        #{'name':'citigroup', 'symbol':'C'},
        #{'name':'salesforce', 'symbol':'CRM'},
        #{'name':'netflix', 'symbol':'NFLX'},
        #{'name':'allergan', 'symbol':'AGN'},
        #{'name':'time warner', 'symbol':'TWX'},
        #{'name':'expedia', 'symbol':'EXPE'},
#skip        {'name':'mastercard', 'symbol':'MA'},
        #{'name':'paypal', 'symbol':'PYPL'},
        #{'name':'broadcom', 'symbol':'AVGO'},
        #{'name':'monsanto', 'symbol':'MON'},
        #{'name':'delta airlines', 'symbol':'DAL'},
        #{'name':'jp morgan', 'symbol':'JPM'},
        #{'name':'t-mobile', 'symbol':'TMUS'},
#skip        {'name':'adobe', 'symbol':'ADBE'},
        #{'name':'activision blizzard', 'symbol':'ATVI'},
#skip        {'name':'dxc technology', 'symbol':'DXC'},
        #{'name':'constellation brands', 'symbol':'STZ'},
        #{'name':'priceline', 'symbol':'PCLN'},
        #{'name':'mgm resorts', 'symbol':'MGM'}, only 10 articles
        #{'name':'nvidia', 'symbol':'NVDA'},
        #{'name':'shire', 'symbol':'SHPG'},
        #{'name':'autodesk', 'symbol':'ADSK'}, few articles
        #{'name':'electronic arts', 'symbol':'EA'},
        #{'name':'wells fargo', 'symbol':'WFC'},
#skip        {'name':'alexion', 'symbol':'ALXN'},
        #{'name':'dell', 'symbol':'DVMT'},
        #{'name':'micron', 'symbol':'MU'},
#skip        {'name':'servicenow', 'symbol':'NOW'},
        #{'name':'zayo', 'symbol':'ZAYO'},  only one article found, but code did not extract it
        #{'name':'aetna', 'symbol':'AET'},
#skip        {'name':'ally financial', 'symbol':'ALLY'},
        #{'name':'anthem', 'symbol':'ANTM'},
        #{'name':'celgene', 'symbol':'CELG'},
        #{'name':'clovis', 'symbol':'CLVS'}, none usable for clovis
        #{'name':'incyte', 'symbol':'INCY'}, none usable
        #{'name':'unitedhealth', 'symbol':'UNH'}, too few
        #{'name':'parsley energy', 'symbol':'PE'} none usable
        ]

started=False
for stock in stock_array:
    process.crawl(cnbcSpider,name=stock['name'],symbol=stock['symbol'])
    process.start()
    started=True
    #process.stop()
    time.sleep(20)

'''
