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
        logger.info("expire key %s" %key)
        return self.rc.expire(key, time)

    def ttl(self, key):
        #get ttl
        logger.info("get ttl")
        return self.rc.ttl(key)

    def hset(self, key, field, value):
        #hash set a key
        logger.info("hset key")
        return self.rc.hset(key, field, value)

    def hget(self, key, field):
        return self.rc.hget(key, field)

    def hgetall(self, key):
        return self.rc.hgetall(key)

    @property
    def ping(self):
        return self.rc.ping()

    @property
    def keys(self):
        return self.rc.keys()

    def Blog2Redis(self, blogs):
        for blog in blogs:
            key = "Team.Front.Blog.Id.%d" %blog.get("id")
            for field, value in blog.iteritems():
                self.rc.hset(key, field, value)
            #self.rc.hgetall(key)

if __name__ == "__main__":
   rc=Redis_connect(host="127.0.0.1", auth='SaintIC') 
   import requests
   res = requests.get("https://api.saintic.com/blog?num=all", verify=False).json()
   print rc.Blog2Redis(res["data"])
