import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured
from info_crawler.util.isearch_redis import RedisMap
from info_crawler.util.isearch_util import get_ip_address_linux
import socket
import time



logger = logging.getLogger(__name__)

class SpiderOpenCloseLogging(object):

    def __init__(self):
        self.items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        settings =  crawler.settings
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured
        crawler_id=settings.getint('MY_CRAWLER_ID')
        # instantiate the extension object
        ext = cls()

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        logging.log(logging.INFO,"opened spider %s", spider.name)

    def spider_closed(self, spider):
        logging.log(logging.INFO,"closed spider %s", spider.name)
        self.url_count(spider)



    def url_count(self,spider):
        redis_db=RedisMap(name="state",namespace="info")
        #local_ip = socket.gethostbyname(socket.gethostname())
        local_ip = get_ip_address_linux("eth0")
        local_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        local_type=1
        local_count = spider.get_count()
        redis_db.set(local_ip,[local_type,local_time,local_count])
