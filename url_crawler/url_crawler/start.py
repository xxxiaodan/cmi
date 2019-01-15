from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import logging
import os
from scrapy.utils.log import configure_logging

# start signal
s=open('signal.txt', 'w')
s.write('start')
s.close()

# del the old logs while config new one
# os.system('rm -f logs.txt')
configure_logging(install_root_handler=False)
logging.basicConfig(filename='logs.txt', format='%(levelname)s: %(message)s', level=logging.INFO)

# start a spider
process = CrawlerProcess(get_project_settings())
process.crawl('isearchSpider')
process.start()

# end signal
f = open('signal.txt', 'w')
f.write("over")
f.close()


