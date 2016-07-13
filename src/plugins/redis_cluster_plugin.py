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

    @property
    def cluster_info(self):
        return self.rc.cluster_info()
