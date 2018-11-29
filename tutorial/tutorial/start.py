# -*- coding: UTF-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import logging
import os
from scrapy.utils.log import configure_logging



configure_logging(install_root_handler=False)
logging.basicConfig(filename='logs.txt',format='%(levelname)s: %(message)s',level=logging.INFO)

process = CrawlerProcess(get_project_settings())
process.crawl('dmoz')
process.start()


