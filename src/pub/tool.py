# -*- coding:utf8 -*-

import re
import hashlib
from log import Syslog
from db import DB
import binascii, os, uuid

md5           = lambda pwd:hashlib.md5(pwd).hexdigest()
mysql         = DB()
logger        = Syslog.getLogger()
gen_token     = lambda :binascii.b2a_base64(os.urandom(24))[:32]
gen_requestId = lambda :str(uuid.uuid4())

#API所需要的正则表达式
mail_check    = re.compile(r'([0-9a-zA-Z\_*\.*\-*]+)@([a-zA-Z0-9\-*\_*\.*]+)\.([a-zA-Z]+$)')
chinese_check = re.compile(u"[\u4e00-\u9fa5]+")

#API所需要的公共函数
def dbUser(username=None, password=False, token=False, uid=False):
    """
    1. 获取数据库中所有用户或是否存在某个具体用户(方法: username=username)。
    2. 当username为真，password=True, 获取用户及密码。
    3. 当username为真，token=True，获取用户及token。
    4. 当username为真，password、token皆为True，获取用户、密码、token。
    5. 当username不存在，即第一条解释。
    """
    if username:
        if password == True:
            if token == True:
                sql = "SELECT username,password,token FROM user WHERE username='%s'" % username
            else:
                sql = "SELECT username,password FROM user WHERE username='%s'" % username
        else:
            if token == True:
                sql = "SELECT username,token FROM user WHERE username='%s'" % username
            else:
                sql = "SELECT username FROM user WHERE username='%s'" % username
    else:#All user from mysql(team.user)
        sql = "SELECT username FROM user"
    logger.info({"func:dbUser:sql":sql})
    try:
        data = mysql.get(sql)
    except Exception, e:
        logger.warn(e)
        logger.error({"func:dbUser:exec_sql":sql})
        return None
    else:
        return data

def postData(request, res):
    logger.debug(request.headers)
    logger.debug(request.json)
    logger.debug(request.form)
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        email    = request.json.get('email', None)
    except Exception,e:
        logger.warn("No request.json, start request.form, get exceptions %s"%e)
        try:
            username = request.form.get('username', None)
            password = request.form.get('password', None)
            email    = request.form.get('email', None)
        except Exception, e:
            logger.error(e)
            res['msg'] = 'No username or password in request, you maybe set headers with "Content-Type: application/json" next time.'
            res['code']= code + 1
    return {"data":(username, password, email), "res": res}

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    _cn = "Mr.tao先生"
    _cn = unicode(_cn)
    res = chinese_check.search(_cn)
    if res:
        print "has Chinese"
    else:
        print 'no Chinese'
