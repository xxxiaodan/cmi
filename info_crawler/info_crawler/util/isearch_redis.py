# -*- coding: utf-8 -*-


import redis
import info_crawler.settings as setting
class IsearchRedis(object):
    """Simple Queue with Redis Backend"""
    def __init__(self, name='urls', namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""  
        self.__db= redis.Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT,db=setting.REDIS_DB, password=setting.REDIS_PASS)
        self.key = '%s:%s' %(namespace, name)  
  
    def qsize(self):  
        """Return the approximate size of the queue."""  
        return self.__db.llen(self.key)  
  
    def empty(self):  
        """Return True if the queue is empty, False otherwise."""  
        return self.qsize() == 0  
  
    def put(self, item):  
        """Put item into the queue."""  
        self.__db.rpush(self.key, item)  
  
    def get(self, block=True, timeout=None):  
        """Remove and return an item from the queue.  
 
        If optional args block is true and timeout is None (the default), block 
        if necessary until an item is available."""  
        if block:  
            item = self.__db.blpop(self.key, timeout=timeout)  
        else:  
            item = self.__db.lpop(self.key)  
  
        if item:  
            item = item[1]  
        return item  
  
    def get_nowait(self):  
        """Equivalent to get(False)."""  
        return self.get(False)


class RedisMap(object):
    def __init__(self, name='urls', namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db= redis.Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT,db=setting.REDIS_DB, password=setting.REDIS_PASS)
        self.key = '%s:%s' %(namespace, name)

    def set(self,key,value):
        self.__db.set(key,value)

    def get(self,key):
        return self.__db.get(key)

    def delete(self,key):
        self.__db.delete(key)

    def size(self):
        return self.__db.dbsize()

    def flushdb(self):
        self.__db.flushdb()

    def exists(self,key):
        self.__db.exists(key)
