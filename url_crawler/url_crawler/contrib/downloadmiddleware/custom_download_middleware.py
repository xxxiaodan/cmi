# -*- coding: UTF-8 -*-
'''
Created on 2014-12-24

@author: Lixiaowei
'''
import random
import base64
# from selenium import webdriver
# from scrapy.http import HtmlResponse
# from twisted.protocols.ftp import NEED_ACCT_FOR_LOGIN


class CustomUserAgentsMiddleware(object):
    '''
    扩展原来的用户代理，采用多个用户代理，轮流使用
    '''
    def process_request(self, request, spider):
        ua  = random.choice(USER_AGENTS)  # @UndefinedVariable
        if ua:
            request.headers.setdefault('User-Agent', ua)

class ProxyMiddleware(object):
  def process_request(self, request, spider):
    proxy = random.choice(PROXIES)
    if proxy['user_pass'] is not None:
      request.meta['proxy'] = "http://%s" % proxy['ip_port']
      encoded_user_pass = base64.encodestring(proxy['user_pass'])
      request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
      print "**************ProxyMiddleware have pass************" + proxy['ip_port']
    else:
      print "**************ProxyMiddleware no pass************" + proxy['ip_port']
      request.meta['proxy'] = "http://%s" % proxy['ip_port']
# class CustomJsHandleMiddleware(object):
#     '''
#     js动态处理，获取js动态加载的数据
#     '''
#     def process_request(self, request, spider):
#         #判断是否需要js动态处理
#         need=False
#         if len( MyConfig.jsHandleRegexObjs )>0:
#             for reg in MyConfig.jsHandleRegexObjs:
#                 if reg.match(request.url):
#                     need = True
#         if need:
#             driver = webdriver.PhantomJS(service_log_path='js.log')
#             driver.get(request.url)
#             html = HtmlResponse(request.url, encoding='utf-8',
#                                 body=driver.page_source.encode('utf-8'))
#             return html


#crawler userAgents list
USER_AGENTS= [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]

PROXIES = [
      {'ip_port': '182.90.77.221:80', 'user_pass': ''},
      {'ip_port': '121.41.161.110:80', 'user_pass': ''},
      {'ip_port': '202.106.16.36:3128', 'user_pass': ''},
      {'ip_port': '183.141.76.54:3128', 'user_pass': ''},
      {'ip_port': '182.88.29.220:8123', 'user_pass': ''},
      ]
