# -*- coding: utf-8 -*-

# Scrapy settings for info_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# ------------------------------------------------user parameter settings---------------------------------------
# Redis
REDIS_HOST = '192.168.0.60'
REDIS_PORT = 6379
REDIS_PASS = 'cs.Swust'
# DB 1 为正在运行 ，0 为测试
#REDIS_DB = 1
REDIS_DB = 0

# mogodb 运行配置
MONGODB_SERVER = '192.168.0.60'
MONGODB_PORT = 27017
# 运行DB 为cmi 测试数据库名为test
#MONGODB_DB = 'cmi'
MONGODB_DB = 'test_cmi'
MONGODB_USER = 'dkelab'
MONGODB_PASS = 'Cs.swust_60'

# -----------------------------------------------------end---------------------------------------------------------



# ---------------------------------------------------system parameter setting-------------------------------------
BOT_NAME = 'info_crawler'

SPIDER_MODULES = ['info_crawler.spiders']
NEWSPIDER_MODULE = 'info_crawler.spiders'


# 使用Redis重写调度器
SCHEDULER = "info_crawler.contrib.extension.scheduler.Scheduler"
SCHEDULER_PERSIST = True

DOWNLOAD_TIMEOUT = 60

# 重定向开启
METAREFRESH_ENABLED = True
REDIRECT_MAX_METAREFRESH_DELAY= 20
REDIRECT_MAX_TIMES = 20
REDIRECT_ENABLED = True
# 重新尝试次数
RETRY_ENANLED=True
RETRY_TIMES = 2

# 禁止cookie
COOKIES_ENABLED = False
# 请求延时
DOWNLOAD_DELAY = 3

MYEXT_ENABLED = True


DOWNLOADER_MIDDLEWARES = {
    'info_crawler.contrib.middleware.custom_download_middleware.CustomUserAgentsMiddleware': 400,
    'scrapy.middleware.useragent.UserAgentMiddleware': None,
}

EXTENSIONS = {
    'info_crawler.contrib.extension.isearch_extension.SpiderOpenCloseLogging': 500,
}
ITEM_PIPELINES = {
    'info_crawler.pipelines.MongoInsertPipeline': 300,
    }
# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#     'info_crawler.contrib.middleware.http_error_middleware.MyHttpErrorMiddleware':543,
#     'scrapy.spidermiddleware.httperror.HttpErrorMiddleware': None,
# }
# -----------------------------------------------------end---------------------------------------------------
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'info_crawler (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN=16
CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED=False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }



# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'info_crawler.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'info_crawler.pipelines.SomePipeline': 300,
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
