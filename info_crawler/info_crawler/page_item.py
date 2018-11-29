# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PageItem(scrapy.Item):
    url = scrapy.Field()  #对应爬取的url
    title = scrapy.Field()  #标题
    content = scrapy.Field()  #正文
    author = scrapy.Field()   #作者
    public_time = scrapy.Field()  #发布时间
    crawl_time = scrapy.Field()  #爬取时间
    site_name = scrapy.Field()   #站点
    section_name = scrapy.Field()  #板块
    site_type=scrapy.Field()  #网站类型

