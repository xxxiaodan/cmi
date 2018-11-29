import scrapy
import re


# rule_dict = {'code': 'UTF-8',
#                'site_name':  '\r\n\xe5\x9b\xbd\xe9\x98\xb2\xe7\xa7\x91\xe6\x8a\x80\xe7\xbd\x91',
#                'public_time_target':  "//*[@class='info_main']/descendant::li[1]/text()",
#                'url':  'https://www.81tech.com/jungong-jishu/201805/23/jishu46262.html',
#                'author_target':  None,
#                'section_name':  '\xe5\x9b\xbd\xe9\x98\xb2\xe7\xa7\x91\xe6\x8a\x80\xe7\xbd\x91-\xe5\x86\x9b\xe4\xba\x8b\xe7\x94\xb5\xe5\xad\x90\xe6\x8a\x80\xe6\x9c\xaf',
#                'title_target':  '//*[@class="info900"]/div/h1/text()',
#                'content_target':  '//*[@id="content"]',
#                'site_type':  1L}

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = ['http://jmjh.miit.gov.cn/newsInfoWebMessage.action?newsId=12829692&moduleId=1062']
    #start_urls.append(rule_dict['url'])
    
    def parse(self, response):
        #print response.body //*[@class='info900']/div[@class
        # ='probox']/h1/text() //*[@id="content"]
        
        public_time_target = response.xpath('//*[@id="con_time"]').extract()
        print public_time_target[0]
        content_target = str(response.xpath('//*[@id="con_con"]').extract())
        print content_target
        title_target = response.xpath('//*[@id="con_t"]').extract()
        print title_target[0]
        author_target = response.xpath('').extract()
        print author_target[0]
        '''
        site_list_target = '//*[@id="comp_29"]'
        # site_url_filter = '^/n\d+/c\d+/content.html$'
        #print response.body
        url_str = response.xpath(site_list_target).extract()
        print str(url_str)
        print len(url_str)
        print url_str[0]
        url_patten = re.compile(r'newsInfoWebMessage\.action\?newsId=\d+&moduleId=\d+')
        url_list = url_patten.findall(url_str[0])
        print url_list'''
        
        

