#-*- coding:utf8 -*-

import os
import json
import torndb
import logging.handlers

__all__ = ["GLOBAL", "MYSQL", "BLOG", "Syslog", "DB", "logger"]

def getConf():
    url     = "https://api.saintic.com/conf?username=admin&mysql=true"
    headers = {"token": "7h8l4uiKZEopBxjJHGHGduQYLA42Xfbr", 'Content-Type': 'application/json'}
    try:
        import requests
        _r   = requests.post(url, headers=headers, verify=False)
        data = _r.json()
    except Exception:
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

GLOBAL, MYSQL, BLOG = getConf()

loglevel  = GLOBAL.get('LogLevel', "INFO")
CODE_HOME = os.path.dirname(os.path.abspath(__file__))
class Syslog:

    logger = None
    levels = {
        "DEBUG" : logging.DEBUG,
        "INFO" : logging.INFO,
        "WARNING" : logging.WARNING,
        "ERROR" : logging.ERROR,
        "CRITICAL" : logging.CRITICAL}

    log_level = loglevel
    log_dir = os.path.join(CODE_HOME, 'logs')
    if not os.path.exists(log_dir): os.mkdir(log_dir)
    log_file = os.path.join(log_dir, 'sys.log')
    log_max_byte = 10 * 1024 * 1024;
    log_backup_count = 5
    log_datefmt = '%Y-%m-%d %H:%M:%S'

    @staticmethod
    def getLogger():
        if Syslog.logger is not None:
            return Syslog.logger

        Syslog.logger = logging.Logger("loggingmodule.Syslog")
        log_handler = logging.handlers.RotatingFileHandler(filename = Syslog.log_file,
                              maxBytes = Syslog.log_max_byte,
                              backupCount = Syslog.log_backup_count)
        log_fmt = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt=Syslog.log_datefmt)
        log_handler.setFormatter(log_fmt)
        Syslog.logger.addHandler(log_handler)
        Syslog.logger.setLevel(Syslog.levels.get(Syslog.log_level))
        return Syslog.logger

#instance it
logger = Syslog.getLogger()

class DB():

    """ 封装与操作常用的操作数据库，初始化数据库，相关工具等。 """
    def __init__(self):
        try:
            self.dbc = torndb.Connection(
                           host     = "%s:%s" %(MYSQL.get('Host'), MYSQL.get('Port', 3306)),
                           database = MYSQL.get('Database'),
                           user     = MYSQL.get('User', None),
                           password = MYSQL.get('Passwd', None),
                           time_zone= MYSQL.get('Timezone','+8:00'),
                           charset  = MYSQL.get('Charset', 'utf8'),
                           connect_timeout=3,max_idle_time=5,)
        except Exception, e:
            logger.error(e)

    def get(self, sql):
        try:
            data=self.dbc.get(sql)
        except Exception,e:
            logger.warn(e)
            data=self.dbc.query(sql)
        return data

    def insert(self, sql):
        return self.dbc.insert(sql)

    def delete(self, sql):
        return self.dbc.execute(sql)

    def update(self, sql):
        return self.dbc.update(sql)

    def execute(self, sql):
        return self.dbc.execute(sql)


if __name__ == "__main__":
    pass
