from scrapy.spiders import BaseSpider
from stockBot.items import cnbcStockbotItem
import datetime # must also import in models.py
import scrapy
import re
import uuid
from bs4 import BeautifulSoup as bsObj
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class cnbcSpiderWeb(scrapy.Spider):
    name = "cnbcSpiderWeb"
    allowed_domains = ['cnbc.com']

    def __init__(self,*args,**kwargs):
        super(cnbcSpiderWeb, self).__init__(*args,**kwargs)
        self.stock=kwargs.get('stock')
        self.unique_id=kwargs.get('task_id')
        self.stockTicker=kwargs.get('symbol')
        if not self.stock:
            self.stock='apple'
        if not self.stockTicker:
            self.stockTicker='AAPL'
        if not self.unique_id:
            self.unique_id='defaultUniqueIDapple'


    def start_requests(self):
        print "cnbcSpiderWeb starting request"
        print self.stock
        #print self.symbol
        url='https://search.cnbc.com/rs/search/view.html?source=CNBC.com&categories=exclude&partnerId=2000&pubtime=0&keywords='
        url =url+self.stock
        urls=[url]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse3)

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
            meta_dict['headline']=d['headline']
            meta_dict['postDate']=formatted_date
            meta_dict['link']=d['link'][0]
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
        headline=response.meta['headline'][0]
        postDate=response.meta['postDate']
        link=response.meta['link']
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

        yield cnbcStockbotItem(unique_id=self.unique_id,headline=headline,postDate=postDate,link=link,articleHTML=article_html,stockTicker=self.stockTicker)


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
