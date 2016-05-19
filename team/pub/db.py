#-*- coding:utf8 -*-

import os
import sys
import torndb
import LOG
from Config import MYSQL

logger = LOG.Syslog.getLogger()
MySQLConnection = MYSQL.get('MySQLConnection')
class DB():

    """ 封装与操作常用的操作数据库，初始化数据库，相关工具等。 """
    def __init__(self):
        try:
            self.dbc = torndb.Connection(
                           host=MySQLConnection.get('Host') + ':' + str(MySQLConnection.get('Port', 3306)),
                           database=MySQLConnection.get('Database', None),
                           user=MySQLConnection.get('User', None),
                           password=MySQLConnection.get('Passwd', None),
                           connect_timeout=30,max_idle_time=60,
                           time_zone=MySQLConnection.get('Timezone','+8:00'),
                           charset=MySQLConnection.get('Charset', 'utf8'))
        except Exception, e:
            logger.error(e)
            sys.exit(126)

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
    sql="select id,title,author,tag,time from blog.blog union select id,Author,Project,GitHub,Language from public.project;"
    sql=' SELECT class FROM blog UNION SELECT ClassName FROM class;'
    print sql
    def ClassData(sql=sql):
        #logger.info(sql)
        types=DB().get(sql)
        classdata={}.fromkeys([ _type.get('class') for _type in types if _type.get('class') ]).keys()
        return classdata
    print ClassData()
