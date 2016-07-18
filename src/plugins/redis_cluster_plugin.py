#-*- coding:utf8 -*-

import sys
from pub import logger

class Redis_cluster_connect(object):

    def __init__(self, host, port):
        try:
            from rediscluster import StrictRedisCluster
        except ImportError,e:
            logger.error(e)
            raise ImportError('%s, maybe you need to install `redis-py-cluster`.' %e)
        else:
            self.rc = StrictRedisCluster(startup_nodes=[{"host": host, "port": port}], decode_responses=True, socket_timeout=3)

    def set(self, key, value, time=3600):
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

    @property
    def cluster_info(self):
        return self.rc.cluster_info()

    def Blog2Redis(self, blogs):
        for blog in blogs:
            key = "Team.Front.Blog.Id.%d" %blog.get("id")
            print key
            for field, value in blog.iteritems():
                self.rc.hset(key, field, value)
            print self.rc.hgetall(key)

if __name__ == "__main__":
   rc=Redis_cluster_connect(host="127.0.0.1", port=10101) 
   import requests
   res = requests.get("https://api.saintic.com/blog?num=all", verify=False).json()
   print rc.Blog2Redis(res["data"])
