#-*- coding:utf8 -*-

import torndb
from tool import logger
from config import MYSQL

class DB():

    """ 封装与操作常用的操作数据库，初始化数据库，相关工具等。 """
    def __init__(self):
        try:
            self.dbc = torndb.Connection(
                           host     = "%s:%s" %(MySQL.get('Host'), MySQL.get('Port', 3306)),
                           database = MySQL.get('Database'),
                           user     = MySQL.get('User', None),
                           password = MySQL.get('Passwd', None),
                           time_zone= MySQL.get('Timezone','+8:00'),
                           charset  = MySQL.get('Charset', 'utf8'),
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
