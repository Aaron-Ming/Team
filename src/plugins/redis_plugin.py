#-*- coding:utf8 -*-

import redis
from pub import logger

class Redis_connect(object):

    def __init__(self, host, port=6379, auth=None):
        self.rc = redis.Redis(host=host, port=port, password=auth, socket_timeout=3, socket_connect_timeout=3, retry_on_timeout=1)

    def set(self, key, value, time=3360):
        #set a key <=> value
        logger.info("Record a k/v for %s,%s" %(key, value))
        self.rc.set(key, value)
        self.expire(key, time)
        return value

    def get(self, key):
        #get a value of key
        logger.info("Query a key for %s " %key)
        return self.rc.get(key)

    def delete(self, *keys):
        #delete a key or more
        logger.info("Delete a key for %s" %key)
        return self.rc.delete(keys)

    def info(self, section=None):
        #get redis info, you can get some section
        logger.info("Get info, section for %s" %section)
        return self.rc.info(section)

    def expire(self, key, time=3600):
        #expire a key
        logger.info("expire key")
        return self.rc.expire(key, time)

    def ttl(self, key):
        #get ttl
        logger.info("get ttl")
        return self.rc.ttl(key)

    @property
    def ping(self):
        return self.rc.ping()

    @property
    def keys(self):
        return self.rc.keys()
