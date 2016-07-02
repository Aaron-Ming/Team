#-*- coding:utf8 -*-

__all__ = ["GLOBAL", "PRODUCT", "BLOG"]

#全局配置端
GLOBAL={

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


def getConf():
    import json
    import requests
    url     = "https://api.saintic.com/conf?username=admin&mysql=true"
    headers = {"token": "7h8l4uiKZEopBxjJHGHGduQYLA42Xfbr", 'Content-Type': 'application/json'}
    try:
        _r   = requests.post(url, headers=headers, verify=False)
        data = _r.json()
    except Exception,e:
        from sh import curl
        data = curl("-s", "-L", "-H", "Content-Type: application/json", "-H", "token:%s"%headers.get("token"), "-X", "POST", url)

    if type(data) is dict:
        C3 = data.get("C3")
    else:
        for _j in data:
            C3 = json.loads(_j).get("C3")
            break
    if not isinstance(C3, dict):
        raise TypeError("C3 not dict when access conf api")

    return C3.get("GLOBAL"), C3.get("MYSQL"), C3.get("BLOG")
#GLOBAL, MYSQL, BLOG = getConf()

