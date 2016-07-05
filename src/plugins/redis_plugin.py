#-*- coding:utf8 -*-

import sys

class Redis_connect(object):

    def __init__(self, host, port=6379, auth=None):
        self.rc = redis.Redis(host=host, port=port, password=auth, socket_timeout=3, socket_connect_timeout=3, retry_on_timeout=1)

    def set(self, key, value):
        pass

    def get(self, key):
        pass
