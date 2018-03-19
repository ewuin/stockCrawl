from scrapy.spiders import BaseSpider
from stockBot.items import bloombergStockbotItem
from scrapy.linkextractors import LinkExtractor
import datetime # must also import in models.py
import scrapy
import re
#import uuid
from bs4 import BeautifulSoup as bsObj
from .sentiment_script_bloomberg import clean_article
from .sentiment_script_bloomberg import sentiment_analysis

class bbSpider(scrapy.Spider):
    name = "bbSpider"

    def __init__(self,*args,**kwargs):
        super(bbSpider, self).__init__(*args, **kwargs)
        self.stock=kwargs.get('stock')
        self.stockTicker=kwargs.get('symbol')
        self.unique_id=kwargs.get('task_id')
        if not self.stock:
            self.stock='apple'
        if not self.stockTicker:
            self.stockTicker='AAPL'
        if not self.unique_id:
            self.unique_id='defaultUniqueIDapple'

    def start_requests(self):
        print self.stock
        print self.stockTicker
        url='https://www.bloomberg.com/search?query='
        url +=self.stock
        urls=[url]

        #urls = [
        #    'http://quotes.toscrape.com/page/1/',
        #    'http://quotes.toscrape.com/page/2/',
        #'https://www.bloomberg.com/search?query=apple',
        #]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse3)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'bb-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


    def get_paragraphs(response_item):
        article_html=""
        divs=response_item.xpath('//div')
        for p in divs.xpath('.//p'):
            article_html+=p.extract()
        return article_html

    def parse_article(self,response):
        print "getting article page html"
        headline=response.meta['headline']
        postDate=response.meta['postDate']
        link=response.meta['link']
        article_type=response.meta['article_type']
        #article_html=response.css('div.body-copy').extract()

        pattern1=re.compile('article')
        pattern2=re.compile('video|audio')

        if re.search(pattern1,article_type):
            article_html=bsObj(response.css('div.body-copy').extract()[0],"html.parser").get_text()
        elif re.search(pattern2,article_type):
            article_html= "audio or video"
        else:
            article_html=get_paragraphs(response)

        if len(article_html)<1:
            article_html=get_paragraphs(response)
        print self.stockTicker
        article_html=u" ".join([i for i in article_html.lower().split()])
        clean_article_html=clean_article(article_html)
        #print article_html has trouble printing ascii character
        article_in_array=[clean_article_html]
        sentiment=sentiment_analysis(article_in_array)
        print sentiment
        yield bloombergStockbotItem(unique_id=self.unique_id,headline=headline,postDate=postDate,link=link,articleHTML=clean_article_html,stockTicker=self.stockTicker,sentiment=sentiment)

    def parse3(self, response):
        for quote in response.css('div.search-result'):
            d={
                'headline': quote.css('h1.search-result-story__headline').xpath('.//a/text()').extract(),
                'post-date': quote.css('time.published-at::attr(datetime)').extract(),
                'link': quote.css('h1.search-result-story__headline').xpath('.//a/@href').extract(),
                'article_type':quote.css('article').xpath('.//@class').extract()
                }
            article_type=str(d['article_type'][0])  #article link will include words video audio or article to inidcate content type
            #next_page_link=quote.css('div.content-page-links').xpath(.//a/@href)

# formatting headline: still has bugs
            if len(d['headline'])>1:
                #print "need to conc headline"
                new_h=""
                for h in d['headline']:
                    #print h
                    try:
                        new_h+=str(h)
                    except:
                        new_h+=" "
                    if d['headline'].index(h)<len(d)-2:
                        new_h+=str(self.stock).title()
                d['headline']=new_h
            else:
                d['headline']=d['headline'][0]
            if d['headline'][0]==" ":
                d['headline']=str(self.stock).title()+d['headline']
            formatted_date=d['post-date'][0]
            formatted_date=formatted_date[:-6]
            #print x
            #print type(x)
            formatted_date=datetime.datetime.strptime(formatted_date,'%Y-%m-%dT%H:%M:%S')

            #print response.css('article').xpath('.//@class').extract()
            meta_dict={
                        'headline':d['headline'],
                        'postDate':formatted_date,
                        'link':d['link'][0],
                        'article_type':article_type
                        }

            yield scrapy.Request(url=d['link'][0],callback=self.parse_article,meta=meta_dict)

## use cmd line prompt: scrapy crawl quotes -o quotes.json to store info as data
## if you reuse filename, it will make file unusable, because it will json the json and
# then append the new results

#alternatively use : scrapy crawl quotes -o quotes.jl
# to append lines of json
