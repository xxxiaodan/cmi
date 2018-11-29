# -*- coding: utf-8 -*-
'''
Created on 2015-11-10

@author: Lixiaowei
'''
import redis
import url_crawler.settings as settings
class RedisUtil(object):
    """Simple Queue with Redis Backend"""  
    def __init__(self, name='urls', namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""  
        self.__db= redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,db=settings.REDIS_DB,password=settings.REDIS_PASS)
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
        self.__db= redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,db=settings.REDIS_DB,password=settings.REDIS_PASS)
        self.key = '%s:%s' %(namespace, name)

    def set(self,key,value):
        self.__db.set(key,value)

    def get(self,key):
        self.__db.get(key)

    def delete(self,key):
        self.__db.delete(key)

    def size(self):
        return self.__db.dbsize()

    def flushdb(self):
        self.__db.flushdb()

    def exists(self,key):
        self.__db.exists(key)
