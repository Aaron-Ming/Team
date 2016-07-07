# -*- coding:utf8 -*-
#plugins open interface

from pub.config import PLUGINS
from redis_plugin import Redis_connect
from redis_cluster_plugin import Redis_cluster_connect

__all__ = ["session_redis_connect", ]

_session_type = PLUGINS.get("session_cluster").get("type")
_session_host = PLUGINS.get("session_cluster").get("host")
_session_port = PLUGINS.get("session_cluster").get("port")
_session_auth = PLUGINS.get("session_cluster").get("auth")

if _session_type == "redis_cluster":
    session_redis_connect = Redis_cluster_connect(_session_host, _session_port)
elif _session_type == "redis":
    session_redis_connect = Redis_connect(_session_host, _session_port, _session_auth)
