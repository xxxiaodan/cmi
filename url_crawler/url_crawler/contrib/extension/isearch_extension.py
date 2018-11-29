import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured
from url_crawler.util.isearch_mysql import MysqlUtil
from url_crawler.util.isearch_redis import RedisMap
import socket
import time



logger = logging.getLogger(__name__)

class SpiderOpenCloseLogging(object):

    def __init__(self,crawler_id):
        self.items_scraped = 0
        self.crawler_id =crawler_id

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        settings =  crawler.settings
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured
        crawler_id=settings.getint('MY_CRAWLER_ID')
        # instantiate the extension object
        ext = cls(crawler_id)

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        logging.log(logging.INFO,"opened spider %s", spider.name)
        self.init_crawler(spider)

    def spider_closed(self, spider):
        logging.log(logging.INFO,"closed spider %s", spider.name)
        self.url_count(spider)

    def init_crawler(self,spider):
        db_util = MysqlUtil()
        sql_sections = 'select * from site,section where section.section_site_id =site.id and crawl_enable = 1 and section_crawl_enable=1 and crawler_id = %d' %(self.crawler_id)
        #sql_proxy = 'select  *  from proxy limit 10'
        section_list=db_util.getAll(sql_sections)
        if section_list is not None and section_list is not False:
            start_urls=[]
            rules=[]
            for section in section_list:
                section_model={}
                section_model['site_name']=section['site_name']
                section_model['section_name']=section['section_name']
                section_model['section_seed_url']=section['section_seed_url']
                section_model['code']=section['code']
                section_model['site_type']=section['site_type']
                if section['section_url'] is not None and section['section_url'] is not '':
                    section_model['site_url']=section['section_url']
                else:
                    section_model['site_url']=section['site_url']
                if section['section_url_filter'] is not None and section['section_url_filter'] is not '':
                    section_model['section_url_filter']=section['section_url_filter']
                else:
                    section_model['section_url_filter']=section['site_url_filter']
                if section['section_list_target'] is not None and section['section_list_target'] is not '':
                    section_model['section_list_target']=section['section_list_target']
                else:
                    section_model['section_list_target']=section['site_list_target']

                if section['section_title_target'] is not None and section['section_title_target'] is not '':
                    section_model['section_title_target']=section['section_title_target']
                else:
                    section_model['section_title_target']=section['site_title_target']

                if section['section_author_target'] is not None and section['section_author_target'] is not '':
                    section_model['section_author_target']=section['section_author_target']
                else:
                    section_model['section_author_target']=section['site_author_target']

                if section['section_content_target'] is not None and section['section_content_target'] is not '':
                    section_model['section_content_target']=section['section_content_target']
                else:
                    section_model['section_content_target']=section['site_content_target']

                if section['section_public_time_target'] is not None and section['section_public_time_target'] is not '':
                    section_model['section_public_time_target']=section['section_public_time_target']
                else:
                    section_model['section_public_time_target']=section['site_public_time_target']
                start_urls.append(section_model['section_seed_url'])
                rules.append(section_model)
            spider.set_start_urls(start_urls)
            spider.set_rules(rules)
        db_util.close()

    def url_count(self,spider):
        redis_db=RedisMap(name="state",namespace="info")
        local_ip = socket.gethostbyname(socket.gethostname())
        local_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        local_type=1
        local_count = spider.get_count()
        redis_db.set(local_ip,[local_type,local_time,local_count])
