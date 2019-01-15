#-*-coding: utf-8 -*-
import logging
import re
import chardet
import scrapy
from url_crawler.util.isearch_redis import RedisUtil

class IsearchSpider(scrapy.Spider):
    name = 'isearchSpider'
    start_urls = []
    redisUrl = RedisUtil()
    rules=[]
    proxys=[]

    #提取的url计数
    url_count=0

    def __init__(self):
        self.start_urls=[]
        self.rules =[]
        super(IsearchSpider,self).__init__()

    def  set_start_urls(self,start_urls=None):
        self.start_urls=start_urls

    def  set_rules(self,rules=None):
        self.rules=rules

    def set_proxys(self,proxys=None):
        self.proxys=proxys

    def get_count(self):
        return self.url_count

    def parse(self, response):
        logging.log(logging.INFO,'A response from %s just arrived!' % response.url)
        #异常情况
        if response is None or response.body is None or response.body=='':
            return
        for section in self.rules:
            if section['section_seed_url'] == response.url:
                #编码问题解决
                self.encodeHandle(response, section['code'])
                #开始解析页面中的url
                result_urls=self.find_links(response, section)
                self.url_count=self.url_count+result_urls.__len__()
                #将抽取到的linkUrl加入url队列中
                self.queue_urls(result_urls, section)
                break


    #从指定的html块儿中提取link_url并补全
    def find_links(self,response,page_info):
        result_list=[]
        link_pattern=re.compile("href=\"(.+?)\"") #构造正则表达式提取文本中的url
        if page_info['section_list_target'] is not None and page_info['section_url_filter'] is not None:
            html_string=str(response.xpath(page_info['section_list_target']).extract()) #xpath抽取指定块中的html文本的url
            #判定块中的文本是否为空
            if html_string == None or html_string == '':
                logging.log(logging.WARNING,'The LinkExtract of html string is empty：'+ page_info['site_list_target'])
                return
            else:
                url_list=link_pattern.findall(html_string)
                # 判定抽取出的link长度
                if len(url_list) <= 0:
                    logging.log(logging.WARNING, 'The LinkExtract of list is empty：'+ page_info['site_list_target'])
                    return
                else:
                    url_filter=re.compile(page_info['section_url_filter'])
                    for i in range(len(url_list)):
                        match=url_filter.match(url_list[i])
                        if match is not None:
                            url=url_list[i]
                            if url.startswith("/"):
                                url=page_info['site_url']+url[1:]
                            elif url.startswith("."):
                                for i in range(len(url)):
                                    if url[i].isalpha() or url[i].isdigit():
                                        url=page_info['site_url']+url[i:]
                                        break
                            elif (url[0].isalpha() or url[i].isdigit()) and (not url.startswith("http")):
                                url = page_info['site_url']+url
                            url = re.sub(r'&amp;', '&', url) #消除某些网站添加&amp;的扒机制
                            logging.log(logging.INFO,"Get url:"+url)
                            result_list.append(url)
                    return result_list

        else:
            logging.log(logging.WARNING, 'The LinkExtract of rule or filter is empty：'+page_info['site_url'])
            return



    def queue_urls(self,url_list,page_info):
        extract_page_info = {}
        for url in url_list:
            # print page_info
            extract_page_info['url']=url
            extract_page_info['site_name']=page_info['site_name']
            extract_page_info['section_name']=page_info['section_name']
            extract_page_info['public_time_target']=page_info['section_public_time_target']
            extract_page_info['content_target']=page_info['section_content_target']
            extract_page_info['title_target']=page_info['section_title_target']
            extract_page_info['author_target']=page_info['section_author_target']
            extract_page_info['code']=page_info['code']
            extract_page_info['site_type']=page_info['site_type']
            self.redisUrl.put(extract_page_info)

    def encodeHandle(self,response,siteCode):
        #尝试解决乱码
        #log.msg('\npreBody:'+response.body, log.ERROR)
        headers=response.headers
        #print('source headers:'+str(headers))
        sourceCode=siteCode
        if hasattr(response, 'encoding'):
            sourceCode = response.encoding
        tempBody=response.body
        end1=tempBody.find('<body')
        end2=tempBody.find('<BODY')
        end3=tempBody.find('</head>')
        end4=tempBody.find('</HEAD>')
        end=end1
        if end==-1:
            end=end2
        if end==-1:
            end=end2
        if end==-1:
            end=end3
        if end==-1:
            end=end4
        if end>0:
            temp=chardet.detect((response.body)[0:end])
            if temp and 'encoding' in temp:
                #print('detect:'+str(temp))
                webCode=temp['encoding'].upper()
                #print('init webcode:'+webCode)
                if webCode!='UTF-8':
                    if webCode.startswith('ISO') or webCode.startswith('ASCII'):
                        webCode=sourceCode
                    try:
                        tempBody=(response.body).decode(webCode).encode('UTF-8')
                        headers['Content-Type']=['text/html; charset='+webCode]
                        response.replace(body=tempBody,headers=headers)
                    except Exception:
                        webCode='GBK'
                        try:
                            tempBody=(response.body).decode(webCode).encode('UTF-8')
                            headers['Content-Type']=['text/html; charset='+webCode]
                            response.replace(body=tempBody,headers=headers)
                        except Exception:
                            webCode='GB2312'
                            tempBody=(response.body).decode(webCode,'ignore').encode('UTF-8')
                            headers['Content-Type']=['text/html; charset='+webCode]
                            response.replace(body=tempBody,headers=headers)
