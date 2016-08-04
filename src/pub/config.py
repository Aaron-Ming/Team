#-*- coding:utf8 -*-

import os

#全局配置端
GLOBAL={

    "Host": os.environ.get("host", "0.0.0.0"),
    #Application run network address, you can set it `0.0.0.0`, `127.0.0.1`, ``;

    "Port": os.environ.get("port", 10050),
    #Application run port, default port;

    "Debug": os.environ.get("debug", True),
    #The development environment is open, the production environment is closed, which is also the default configuration.

    "LogLevel": os.environ.get("loglevel", "DEBUG"),
    #应用程序写日志级别，目前有DEBUG，INFO，WARNING，ERROR，CRITICAL

    "put2Redis": os.environ.get("put2redis", True),
    #是否开启put至redis的线程
}


#生产环境配置段
PRODUCT={

    "ProcessName": "Team.Front",
    #Custom process, you can see it with "ps aux|grep ProcessName".

    "ProductType": os.environ.get("producttype", "tornado"),
    #生产环境启动方法，可选`gevent`, `tornado`。
}


#博客配置项
BLOG={
   "IndexPageNum": 8,
    #首页文章展现术,
    "AdminGroup": ("admin", "taochengwei"),
    #管理员权限组
}

#插件配置项
PLUGINS={
    "session_cluster": os.environ.get("session_cluster", {
        "type": "redis_cluster",
        #指定session集群，暂时支持redis、redis cluster,
        "host": "127.0.0.1",
        #指定session集群存储应用host/ip,
        "port": 10101,
        #指定session集群存储应用port,
        "auth": None
        #验证密码(目前仅支持单实例版redis)
        }),
}
