#-*- coding:utf8 -*-
#Conection Redis Module.

from pub import logger
try:
    import redis
    import rediscluster
except ImportError,e:
    logger.error(e)
    raise ImportError('%s, maybe you need to install `redis-py-cluster`.' %e)


class RedisBaseApi(object):

    def __init__(self, sessionType, **kw):
        host = kw.get("host")
        port = kw.get("port")
        auth = kw.get("pass")
        rc1 = lambda host, port, auth=None: redis.Redis(host=host, port=port, password=auth, socket_timeout=3, socket_connect_timeout=3, retry_on_timeout=3)
        rc2 = lambda host, port: rediscluster.StrictRedisCluster(startup_nodes=[{"host": host, "port": port}], decode_responses=True, socket_timeout=3)
        if sessionType == "redis":
            self.rc = rc1(host, port, auth)
        elif sessionType == "redis_cluster":
            self.rc = rc2(host, port)

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