import scrapy
import re
class DmozSpider(scrapy.Spider):
    name = "proxy"
    allowed_domains = ["proxy.org"]
    start_urls = ['http://www.sastind.gov.cn/n157/index.html']
    # for i in range(1, 4):
    #     url_str = 'http://www.xicidaili.com/nn/%s' % i
    #     start_urls.append(url_str)
    #
    def parse(self, response):
        # print response.body //*[@class='info900']/div[@class
        # ='probox']/h1/text()
        
        content = response.xpath('//*[@id="comp_3768"]/table[2]/tbody').extract()
        print content
  




