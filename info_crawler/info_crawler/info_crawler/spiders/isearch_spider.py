#-*-coding: utf-8 -*-
import datetime
import logging
import time
import chardet
import scrapy
import re
import info_crawler.util.isearch_tools as tool
from info_crawler.page_item import PageItem
from info_crawler.util.isearch_redis import IsearchRedis
from info_crawler.util.isearch_redis import RedisMap
from info_crawler.util.isearch_util import get_ip_address_linux
import sys


reload(sys)
sys.setdefaultencoding('utf8')
title_rule = '/html/head/title/text()'


class IsearchSpider(scrapy.Spider):
    name = 'isearchSpider'
    start_urls = ['http://www.baidu.com']
    url_count = 0

    def get_count(self):
        return self.url_count

    def __init__(self):
        self.redisUrl = IsearchRedis()
        self.redisMap = RedisMap(name="state", namespace="info")
        self.local_ip = get_ip_address_linux("eth0")
        state = eval(self.redisMap.get(self.local_ip))
        if state is not None:
            self.url_count = state[2]
        self.run = True
        super(IsearchSpider, self).__init__()

    def parse(self, response):
        while self.run:
            page = eval(self.redisUrl.get())  #种子队列中的结构化种子信息
            # print page
            if page is not None:
                self.local_state()
                page_url = page['url']  #种子url
                if page_url.startswith("http"):
                    yield scrapy.Request(url=page_url, meta={'page_info': page}, callback=self.parse_info_page)
                    # print page_url
            # time.sleep(15)

    def parse_info_page(self, response):
        '''
        抽取列表中的url信息
        '''
        page_info = response.meta['page_info']
        logging.log(logging.INFO, 'A response from %s just arrived!' % response.url)
        # 异常情况
        if response is None or response.body is None or response.body=='':
            logging.log(logging.WARNING, 'The response from %s is empty!' % response.url)
            return
        # 编码问题解决
        self.encodeHandle(response, page_info['code'])

        # 开始解析页面中信息
        page = self.extract_page_info(response, page_info)
        self.url_count += 1
        return page

    # 从指定的html块儿中提取link_url并补全
    def extract_page_info(self, response, page_info):
        page = PageItem()
        page['url']=page_info['url']
        page['title']=''
        page['author']=''
        page['content']=''
        page['public_time']=''
        page['crawl_time']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        page['site_name']=page_info['site_name']
        page['section_name']=page_info['section_name']
        page['site_type']=page_info['site_type']

        #抽取题目
        try:
            if page_info['title_target'] is not None:
                page['title'] = str(response.xpath(page_info['title_target']).extract()[0]) #xpath抽取指定块中的html文本的url
            else:
                logging.log(logging.WARNING,'The LinkExtract of title rule is empty：'+ page_info['title_target'])
                page['title'] = str(response.xpath(title_rule).extract()[0])
        except Exception as e:
            logging.log(logging.ERROR,'The LinkExtract of title raise exception：'+e.message)

        #若用户自定义抽取规则无法提取，则采用默认的抽取规则
        if page['title'] is None or page['title'] == '':
            page['title'] = str(response.xpath(title_rule).extract()[0])
        page['title'] = tool.ISearchTools.strip_tags(page['title'])

        #抽取作者
        try:
            if page_info['author_target'] is not None:
                page['author'] = str(response.xpath(page_info['author_target']).extract()[0]) #xpath抽取指定块中的html文本的url
                page['author'] = re.sub(u'作者：', '', page['author'])
            else:
                logging.log(logging.WARNING,'The LinkExtract of author rule is empty：'+ page_info['author_target'])
        except Exception as e:
            logging.log(logging.ERROR, 'The LinkExtract of author raise exception：'+e.message)

        # 抽取正文
        try:
            if page_info['content_target'] is not None:
                #page['content']=str(response.xpath(page_info['content_target']).extract()[0]) #old 为适应利用兄弟节点定位，修改如下
                page['content']=str(response.xpath(page_info['content_target']).extract()[0]) #xpath抽取指定块中的html文本的url
            else:
                logging.log(logging.WARNING,'The LinkExtract of content rule is empty：'+ page_info['content_target'])
        except Exception as e:
            logging.log(logging.ERROR,'The LinkExtract of content raise exception：'+e.message)

        # 若用户自定义抽取规则无法提取，则采用基于文本密度的正文抽取方法粗略抽取
        if page['content'] is None or page['content'] == '':
            page['content'] = str(tool.ISearchTools.extractHtmlText(response.body))
        # 标签清洗
        # page['content'] = tool.ISearchTools.extractHtmlText(page['content']).replace(' ', '')
        # print(len(page['content']))
        # 抽取发布时间
        try:
            if page_info['public_time_target'] is not None:
                page['public_time']=tool.ISearchTools.extractDateTimeFromStr(
                    str(response.xpath(page_info['public_time_target']).extract()[0])).decode("unicode_escape")
            else:
                logging.log(logging.WARNING,'The LinkExtract of public time  rule is empty：'+ page_info['public_time_target'])
        except Exception as e:
            logging.log(logging.ERROR, 'The LinkExtract of public time raise exception：'+e.message)

        return page

    def encodeHandle(self, response, siteCode):
        # 尝试解决乱码
        headers = response.headers
        sourcecode = siteCode
        if hasattr(response, 'encoding') and response.encoding.upper() == 'UTF-8':
            pass
        else:
            # web_code = sourcecode
            tempbody = response.body
            end1 = tempbody.find('<body')
            end2 = tempbody.find('<BODY')
            end3 = tempbody.find('</head>')
            end4 = tempbody.find('</HEAD>')
            end = end1
            if end == -1:
                end = end2
            if end == -1:
                end = end2
            if end == -1:
                end = end3
            if end == -1:
                end = end4
            if end > 0:
                temp = chardet.detect(response.body[0:end])
                if temp and 'encoding' in temp:
                    web_code = temp['encoding'].upper()
                    print 'web_code:%s' % web_code
                    if web_code != 'UTF-8':
                        if web_code.startswith('ISO') or web_code.startswith('ASCII'):
                            web_code = sourcecode
                        try:
                            tempbody = (response.body).decode(web_code).encode('UTF-8')
                            headers['Content-Type'] = ['text/html; charset='+web_code]
                            response.replace(body=tempbody,headers=headers)
                        except Exception:
                            web_code = 'GBK'
                            try:
                                tempbody = (response.body).decode(web_code).encode('UTF-8')
                                headers['Content-Type']=['text/html; charset='+web_code]
                                response.replace(body=tempbody,headers=headers)
                            except Exception:
                                web_code = 'GB2312'
                                tempbody = (response.body).decode(web_code, 'ignore').encode('UTF-8')
                                headers['Content-Type'] = ['text/html; charset='+web_code]
                                response.replace(body=tempbody, headers=headers)

    def local_state(self):
        # local_ip = socket.gethostbyname(socket.gethostname())
        local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        local_type = 1
        local_count = self.get_count()
        self.redisMap.set(self.local_ip, [local_type, local_time, local_count])
