#-*- coding:utf8 -*-

#全局配置端
GLOBAL={

    #"Environment": "super debug",
    "Environment": "dev",
    "Environment": "product",
    #1. The meaning of the representative is the application of the environment, the value of dev, product;
    #2. When the value is dev, only exec app.run() with flask.
    #3. When the value is product, will start server with tornado or gevent.
    #3. When the value is "super debug", will start tuning mode.

    "Host": "0.0.0.0",
    #Application run network address, you can set it `0.0.0.0`, `127.0.0.1`, ``, `None`;
    #Default run on all network interfaces.

    "Port": 10050,
    #Application run port, default port;

    "Debug": True,
    #The development environment is open, the production environment is closed, which is also the default configuration.

    "LogLevel": "DEBUG",
    #应用程序写日志级别，目前有DEBUG，INFO，WARNING，ERROR，CRITICAL
}

#生产环境配置段
PRODUCT={

    "ProcessName": "Team.Front",
    #Custom process, you can see it with "ps aux|grep ProcessName".

    "ProductType": "tornado",
    #生产环境启动方法，可选`gevent`, `tornado`, `uwsgi`,其中tornado log level是WARNNING，也就是低于WARN级别的日志不会打印或写入日志中。
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
    "session_cluster": {
        "type": "redis_cluster",
        #指定session集群，暂时支持redis、redis cluster,
        "host": "127.0.0.1",
        #指定session集群存储应用host/ip,
        "port": 10101,
        #指定session集群存储应用port,
        "auth": None
        #验证密码(目前仅支持单实例版redis)
        },
}
