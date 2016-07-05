#-*- coding:utf8 -*-

import sys
from pub import logger

class Redis_cluster_connect(object):

    def __init__(self, cluster_host, cluster_port):
        try:
            from rediscluster import StrictRedisCluster
        except ImportError,e:
            logger.error(e)
            raise ImportError('%s, maybe you need to install `redis-py-cluster`.' %e)
        else:
            self.rc = StrictRedisCluster(startup_nodes=[{"host": cluster_host, "port": cluster_port}], decode_responses=True)

    def set(self, key, value):
        return self.rc.set(key, value)

    def get(self, key):
        return self.rc.get(key)
