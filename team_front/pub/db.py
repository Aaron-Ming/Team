#-*- coding:utf8 -*-

import torndb
from tool import logger
from config import MYSQL

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
    mysql=DB()
    data=mysql.get("select email from user")
    print [ email.email for email in data if email.email ]
