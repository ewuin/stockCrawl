import scrapy
from selenium import webdriver

class ProductSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ['cnbc.com']
    start_urls = ['https://search.cnbc.com/rs/search/view.html?source=CNBC.com&categories=exclude&partnerId=2000&keywords=apple']

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self,url): #response):
        self.driver.get(url)#response.url)
        #while True:
        next = self.driver.find_element_by_xpath('//*[@id="rightPagCol"]/a')  #/@href'   or //div[@id="rightPagCol"]/a
            # self.driver.find_element_by_xpath('//td[@class="pagn-next"]/a')
        print next
        try:
            next.click()

                # get the data and write it to scrapy items
        except:
            print("next not clicked")

            #except:
            #    break

        #self.driver.close()

PS = ProductSpider()
PS.parse(PS.start_urls[0])
