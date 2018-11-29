# -*- coding: utf-8 -*-
from twisted.internet.threads import deferToThread
import pymongo
import time
MONGODB_SERVER = '192.168.0.60'
MONGODB_PORT = 27017
MONGODB_DB = 'cmi'
MONGODB_USER = 'dkelab'
MONGODB_PASS = 'Cs.swust_60'


class MongoInsertPipeline(object):
    """Pushes serialized item into a redis list/queue"""

    def __init__(self, server):
        self.server = server

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('MONGODB_SERVER', MONGODB_SERVER)
        port = settings.get('MONGODB_PORT', MONGODB_PORT)
        db = settings.get('MONGODB_DB',MONGODB_DB)
        # collection= settings.get('MONGODB_COLLECTION',MONGODB_COLLECTION)
        user = settings.get('MONGODB_USER', MONGODB_USER)
        password = settings.get('MONGODB_PASS', MONGODB_PASS)
        connection = pymongo.MongoClient(host, port)
        connection.admin.authenticate(user, password)
        server = {"connection": connection, 'db': db}
        return cls(server)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        connection = self.server['connection']
        db = connection[self.server['db']]
        collection = db[time.strftime('%Y-%m-%d', time.localtime(time.time()))]
        collection.insert(dict(item))
        spider.url_count = spider.url_count+1
        return item

    def item_key(self, item, spider):
        """Returns mongodb key based on given spider"""
        return "%s:items" % spider.name
