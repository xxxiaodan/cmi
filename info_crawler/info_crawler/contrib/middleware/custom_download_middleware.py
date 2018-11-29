# -*- coding: UTF-8 -*-
import random
import base64
import requests


class CustomUserAgentsMiddleware(object):
    '''
    扩展原来的用户代理，采用多个用户代理，轮流使用
    '''
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENTS)  # @UndefinedVariable
        if ua:
            request.headers.setdefault('User-Agent', ua)


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        # proxy = judge_activate(http_url=request.url)
        if request.url.startswith("http://"):
            proxy = random.choice(PROXIES)
        else:
            proxy = random.choice(PROXIES_S)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = proxy['url']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        else:
            request.meta['proxy'] = proxy['url']


# crawler userAgents list
USER_AGENTS= [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]

PROXIES = [
    {'url': 'http://121.31.194.120:8123', 'user_pass': ''},
    {'url': 'http://119.250.252.59:8118', 'user_pass': ''},
    {'url': 'http://139.199.38.182:8118', 'user_pass': ''},
    {'url': 'http://113.128.148.50:8118', 'user_pass': ''},
    {'url': 'http://58.53.128.83:3128', 'user_pass': ''},
    {'url': 'http://61.135.217.7:80', 'user_pass': ''},
    {'url': 'http://101.236.57.99:8866', 'user_pass': ''},
    {'url': 'http://222.217.68.51:54355', 'user_pass': ''},
    {'url': 'http://222.184.7.206:40908', 'user_pass': ''},
    {'url': 'http://124.234.157.29:80', 'user_pass': ''},
    {'url': 'http://183.3.150.210:41258', 'user_pass': ''},
    {'url': 'http://120.26.127.90:8118', 'user_pass': ''},
    {'url': 'http://114.225.170.37:53128', 'user_pass': ''},
    {'url': 'http://171.37.163.111:8123', 'user_pass': ''},
    {'url': 'http://61.135.155.82:443', 'user_pass': ''},
    {'url': 'http://117.91.253.119:8118', 'user_pass': ''},
    {'url': 'http://180.121.131.172:3128', 'user_pass': ''},
    {'url': 'http://116.7.176.75:8118', 'user_pass': ''},
    {'url': 'http://42.176.36.251:37000', 'user_pass': ''},
    {'url': 'http://119.254.94.123:50972', 'user_pass': ''},
    {'url': 'http://111.75.223.9:35918', 'user_pass': ''},
    {'url': 'http://171.37.162.223:8123', 'user_pass': ''},
    {'url': 'http://113.116.158.80:808', 'user_pass': ''},
    {'url': 'http://117.21.191.151:61007', 'user_pass': ''},
    {'url': 'http://222.94.147.105:808', 'user_pass': ''},
    {'url': 'http://60.217.64.237:31923', 'user_pass': ''},
    {'url': 'http://61.183.233.6:54896', 'user_pass': ''},
    {'url': 'http://180.168.13.26:8000', 'user_pass': ''},
    {'url': 'http://222.139.245.130:58424', 'user_pass': ''},
    {'url': 'http://221.214.180.122:33190', 'user_pass': ''},
    {'url': 'http://171.34.191.80:8123', 'user_pass': ''},
    {'url': 'http://58.240.224.252:33035', 'user_pass': ''},
    {'url': 'http://122.115.78.240:38157', 'user_pass': ''},
    {'url': 'http://42.48.118.106:50038', 'user_pass': ''},
    {'url': 'http://118.181.226.216:36430', 'user_pass': ''},
    {'url': 'http://116.236.98.78:43682', 'user_pass': ''},
    {'url': 'http://182.90.77.221:80', 'user_pass': ''},
    {'url': 'http://121.41.161.110:80', 'user_pass': ''},
    {'url': 'http://202.106.16.36:3128', 'user_pass': ''},
    {'url': 'http://183.141.76.54:3128', 'user_pass': ''},
    {'url': 'http://182.88.29.220:8123', 'user_pass': ''},
]

PROXIES_S = [
    {'url': 'https://118.190.94.224:9001', 'user_pass': ''},
    {'url': 'https://118.122.92.252:37901', 'user_pass': ''},
    {'url': 'https://123.170.160.214:8888', 'user_pass': ''},
    {'url': 'https://121.225.25.132:3128', 'user_pass': ''},
    {'url': 'https://42.101.22.93:8888', 'user_pass': ''},
    {'url': 'https://106.9.171.109:8010', 'user_pass': ''},
    {'url': 'https://106.14.47.5:80', 'user_pass': ''},
    {'url': 'https://106.86.208.98:41683', 'user_pass': ''},
    {'url': 'https://101.64.32.100:808', 'user_pass': ''},
    {'url': 'https://115.46.98.246:8123', 'user_pass': ''},
    {'url': 'https://120.69.82.110:44693', 'user_pass': ''},
    {'url': 'https://113.108.242.36:47713', 'user_pass': ''},
    {'url': 'https://101.236.55.145:8866', 'user_pass': ''},
    {'url': 'https://117.114.149.66:53281', 'user_pass': ''},
    {'url': 'https://175.148.78.132:1133', 'user_pass': ''},
    {'url': 'https://58.218.201.188:58093', 'user_pass': ''},
    {'url': 'https://171.39.6.113:8123', 'user_pass': ''},
    {'url': 'https://61.187.206.207:46693', 'user_pass': ''},
    {'url': 'https://59.57.151.126:37749', 'user_pass': ''},
    {'url': 'https://115.223.79.209:8010', 'user_pass': ''},
    {'url': 'https://221.232.192.236:8010', 'user_pass': ''},
    {'url': 'https://42.55.254.5:1133', 'user_pass': ''},
    {'url': 'https://61.142.72.154:30074', 'user_pass': ''},
    {'url': 'https://219.234.5.128:3128', 'user_pass': ''},
    {'url': 'https://111.72.155.158:53128', 'user_pass': ''},
    {'url': 'https://175.155.138.182:1133', 'user_pass': ''},
    {'url': 'https://58.62.238.150:32431', 'user_pass': ''},
    {'url': 'https://221.206.100.133:34073', 'user_pass': ''},
    {'url': 'https://222.223.115.30:51618', 'user_pass': ''},
    {'url': 'https://42.51.3.89:8080', 'user_pass': ''},
    {'url': 'https://182.241.226.25:43584', 'user_pass': ''},
    {'url': 'https://106.12.7.54:8118', 'user_pass': ''},
    {'url': 'https://140.207.155.94:52685', 'user_pass': ''},
    {'url': 'https://113.12.202.50:40498', 'user_pass': ''},
    {'url': 'https://121.31.177.220:8123', 'user_pass': ''},
    {'url': 'https://218.24.16.198:43620', 'user_pass': ''},
    {'url': 'https://61.145.69.27:42380', 'user_pass': ''},
    {'url': 'https://115.46.70.76:8123', 'user_pass': ''},
    {'url': 'https://58.254.220.116:52470', 'user_pass': ''},
    {'url': 'https://183.47.2.201:30278', 'user_pass': ''},
    {'url': 'https://60.176.237.88:8888', 'user_pass': ''},
    {'url': 'https://110.189.152.86:52277', 'user_pass': ''},
    {'url': 'https://114.119.116.92:61066', 'user_pass': ''},
    {'url': 'https://218.249.45.162:35586', 'user_pass': ''},
    {'url': 'https://175.175.217.192:1133', 'user_pass': ''},
    {'url': 'https://222.241.190.141:80', 'user_pass': ''},
    {'url': 'https://180.110.6.149:808', 'user_pass': ''},
    {'url': 'https://58.210.133.98:32741', 'user_pass': ''},
    {'url': 'https://121.31.195.113:8123', 'user_pass': ''},
    {'url': 'https://222.183.209.32:8123', 'user_pass': ''},
    {'url': 'https://218.61.203.134:51987', 'user_pass': ''},
    {'url': 'https://124.232.133.201:30819', 'user_pass': ''},
    {'url': 'https://211.147.239.101:57281', 'user_pass': ''},
    {'url': 'https://113.103.13.86:3128', 'user_pass': ''},
    {'url': 'https://119.1.97.193:60916', 'user_pass': ''},
    {'url': 'https://140.207.50.246:51426', 'user_pass': ''},
    {'url': 'https://27.54.248.42:8000', 'user_pass': ''},
    {'url': 'https://121.31.136.255:8123', 'user_pass': ''},
    {'url': 'https://27.17.45.90:43411', 'user_pass': ''},
    {'url': 'https://117.37.30.194:8118', 'user_pass': ''},
    {'url': 'https://183.63.101.62:53281', 'user_pass': ''},
    {'url': 'https://59.32.37.249:61234', 'user_pass': ''},
    {'url': 'https://182.88.162.110:8123', 'user_pass': ''},
    {'url': 'https://125.67.25.83:41681', 'user_pass': ''},
]


def judge_activate(http_url):
    count = 0
    while count<10:
        if http_url.startswith("http://"):
            proxy = random.choice(PROXIES)
            print(http_url)
        else:
            proxy = random.choice(PROXIES_S)
        proxy_dict={}
        proxy_dict['type'] = http_url
        try:
            response = requests.get(http_url, proxies=proxy_dict)
            code = response.status_code
            if 200 <= code < 300:
                print "activate code:%d url: %s " % (code, http_url)
                #return proxy
            else:
                print("invalid ip and port")
        except:
            print('invalid ip and port')
        count += 1
#test_url = 'http://jmjh.miit.gov.cn/newsInfoWebMessage.action?newsId=10744349&moduleId=1062'
# print judge_activate(test_url)