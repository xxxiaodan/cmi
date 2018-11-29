# -*- coding: utf-8 -*-

# Scrapy settings for url_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html


#-------------------------------------------------user parameter set----------------------------------------------------
#初始url种子
start_urls=[]
#初始抽取规则
start_rule=[]
#爬虫的唯一ID,用于爬取的网站分配便于扩展
MY_CRAWLER_ID=1

#Mysql config
DB_HOST ='192.168.0.60'
DB_PORT=3306
DB_USER='root'
#DB_PASSWORD='cs.swust'
DB_PASSWORD = 'Cs.swust123'
DB_NAME='cmi'
DB_CHARSET='UTF8'

#Redis config
REDIS_HOST='192.168.0.60'
REDIS_PORT=6379
REDIS_PASS='cs.Swust'
REDIS_DB=1
#---------------------------------------------------end---------------------------------------------------------





#-------------------------------------------------system parameter set------------------------------------------

BOT_NAME = 'url_crawler'
SPIDER_MODULES = ['url_crawler.spiders']
NEWSPIDER_MODULE = 'url_crawler.spiders'

DOWNLOADER_MIDDLEWARES = {
    'url_crawler.contrib.downloadmiddleware.custom_download_middleware.CustomUserAgentsMiddleware': 400,
    'scrapy.downloadmiddleware.useragent.UserAgentMiddleware': None,
}


DOWNLOAD_TIMEOUT = 60
DUPEFILTER_DEBUG= True
#重定向最大次数
REDIRECT_MAX_TIMES = 2
REDIRECT_ENABLED = True
COOKIES_ENABLED=False
DOWNLOAD_DELAY=0.25
MYEXT_ENABLED=True
#-----------------------------------------------------end---------------------------------------------------------
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'url_crawler (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN=16
CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'url_crawler.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'url_crawler.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'url_crawler.contrib.extension.isearch_extension.SpiderOpenCloseLogging': 500,
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'url_crawler.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
AUTOTHROTTLE_ENABLED=True
# The initial download delay
AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'