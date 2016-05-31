# -*- coding:utf8 -*-

from pub import logger, mysql, gen_token, gen_requestId, md5, config, dbUser, mail_check, chinese_check
from flask import request, g
from flask.ext.restful import Resource
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class User(Resource):
    """User resource, url is /user, /user/.
    1. #get:    Get user
    2. #post:   Create user, registry and login
    3. #put:    Update user profile
    4. #delete: Delete user
    """
    def get(self):
        """Public func, no token, with url args:
        1. num, 展现的数量,默认是10条。
        2. username|email, 用户名或邮箱，数据库主键，唯一。

        返回数据样例，{'msg':'success or error(errmsg)', 'code':'http code', 'data':data, 'url':request_url}
        """
        res={"code": 200, "url": request.url, "msg": None, "data": None}
        try:
            _num = int(request.args.get('num', 10))
        except ValueError, e:
            logger.warn(e)
            res.update({"msg": "the num is not integer", "code": 1000}) #code:1000, for get, the error is num error when request
            return res
        else:
            _email    = request.args.get('email', None)
            _username = request.args.get('username', None)
            _token    = request.args.get('token')
            logger.debug({"email": _email, "username": _username, "token": _token, "requestId": str(g.requestId)})
            if _username: #username's priority is greater than email
                if _token == 'true':
                    sql="SELECT username,email,cname,motto,url,token,extra FROM user WHERE username='%s' LIMIT %d" %(_username, _num)
                else:
                    sql="SELECT username,email,cname,motto,url,extra FROM user WHERE username='%s' LIMIT %d" %(_username, _num)
            elif _email:
                emails=mysql.get("SELECT email FROM user")
                logger.debug({"The first email": emails, "requestId": str(g.requestId)})
                emails=[ email.email for email in emails if email.email ]
                logger.debug({"The second email": emails, "requestId": str(g.requestId)})
                if not _email in emails: #check email in mysql
                    res.update({"msg": "no such email", "code": 1001}) #code:1001, request email not in mysql
                    logger.info(res)
                    return res
                if mail_check.match(_email):
                    if _token == 'true':
                        sql="SELECT username,email,cname,motto,url,token,extra FROM user WHERE email='%s' LIMIT %d" %(_email, _num)
                    else:
                        sql="SELECT username,email,cname,motto,url,extra FROM user WHERE email='%s' LIMIT %d" %(_email, _num)
                else:
                    res.update({"msg": "mail format error", "code": 1002}) #code:1002, email format error with mail.match(re)
                    logger.info(res)
                    return res
            else: #url args no username and email
                if _token == 'true':
                    sql="SELECT username,email,cname,motto,url,token,extra FROM user LIMIT %d" % _num
                else:
                    #this is default sql and display
                    sql="SELECT username,email,cname,motto,url,extra FROM user LIMIT %d" %  _num
            #try...except...else(if...elif...else) is end, write log sql and requestId
            logger.info({"requestId": g.requestId, "User Get End SQL": sql})
        try:
            data=mysql.get(sql)
        except Exception,e:
            logger.error(e)
            res.update({"msg": "get user info error, %s" %e, "code": 1003}) #code:1003, exec sql error from mysql.
        else:
            res.update({"msg": "success", "data": data, "code": 0})
        logger.info(res)
        return res

    def post(self):
        """login and registry, with url args:
        1. action=log/reg, default is log;

        post data:
        1. username,
        2. password,
        3. email,可选, 不用做系统登录, 如果有则会做正则检测不符合格式则弹回请求.
        """
        res = {"url": request.url, "msg": None, "data": None}
        request_json = request.json
        logger.debug({"request.json": request_json, "request.json.type": type(request_json)})
        if request_json: #header ask: "Content-type: application/json"
            username = request_json.get('username', None)
            password = request_json.get('password', None)
            email    = request_json.get('email')
        else:            #this is default form ask
            logger.debug("No request.json, start request.form")
            try:
                username = request.form.get('username', None)
                password = request.form.get('password', None)
                email    = request.form.get('email')
            except Exception, e:
                logger.error(e)
                res.update({'msg': 'No username or password in request', 'code': 1015}) #code:1015, 获取不到相关的请求(username and password)
                return res
        if not username or not password:
            logger.debug({"User:post:request.json(user, pass)": (username, password), "res": res.update({'msg': 'Invaild username or password', 'code': 1016})}) #code:1016, 请求的username或password为空。
            return res
        else:
            res.update({'data': {'username': username, 'email': email}})
        #define username and password length(can be from config.py)
        if len(username) < 5 or len(password) < 5:
            res.update({'msg': 'username or password length of at least 5', 'code': 1010}) #code:1010, username/password length < 5
            logger.warn(res)
            return res
        if chinese_check.search(unicode(username)): #reload(sys), and set defaultencoding('utf8')
            res.update({'msg': 'username contains Chinese, not allowed!', 'code': 1019}) #code:1019,请求的username含有中文
            logger.error(res)
            return res
        if email and mail_check.match(email) == None:
            logger.debug({"User:post:request.json": email, "res": res.update({'msg': "email format error", 'code': 1017})})  #when email has set, otherwise, pass `if...abort`. The code:1017, email format error in request.json.
            return res
        #Start Action with (log, reg)
        _MD5pass = md5(password)
        action   = request.args.get("action") #log or reg (登录or注册)
        ReqData  = dbUser(username, password=True)
        #ReqData is True(user is exists), it's dict, eg:{'username': u'xxxxx', 'password': u'xxxxxxxxxx'}
        logger.debug({"request.action": action, 'ReqData': ReqData})
        if action == 'log':
            #When `ReqData` is True, has user, it's right, continue login
            if not ReqData:
                res.update({'msg':'User not exists', 'code': 1018}) #code:1018, 登录请求时，请求中的username在数据库中获取不到信息(没有此用户)。
                logger.warn(res)
                return res
            try:
                _DBuser  = ReqData.get('username')
                _DBpass  = ReqData.get('password')
            except AttributeError,e:
                logger.error(e)
                res.update({'msg':'User not exists', 'code': 1018}) #code:1018, 登录请求时，请求中的username在数据库中获取不到信息(没有此用户)。
                logger.warn(res)
                return res
            else:
                logger.debug({'ReqUser': username, 'ReqPassMD5': _MD5pass, 'DBuser': _DBuser, 'DBpass': _DBpass})
            if _MD5pass == _DBpass:
                res.update({'msg': 'Password authentication success at sign in', 'code': 0}) #code:0, it's successful
            else:
                res.update({'msg': 'Password authentication failed at sign in', 'code': 1011}) #code:1011, request pass != mysql pass
            logger.info(res)
            return res
        elif action == 'reg':
            #When `ReqData` is True, has user, it's wrong, cannot registry
            if ReqData:
                res.update({'msg': 'User already exists, cannot be registered!', 'code': 1014}) #code:1024, already has user when reg.
                logger.warn(res)
                return res
            try:
                sql = "INSERT INTO user (username, password, email) VALUES('%s', '%s', '%s')" % (username, _MD5pass, email)
                if hasattr(mysql, 'insert'):
                    mysql.insert(sql)
                else:
                    mysql.execute(sql)
                logger.info({"User:post:reg:sql": sql})
            except Exception, e:
                res.update({'code':1012, 'msg':'Sign up failed'}) #code:1012, sign up failed when write into mysql
                logger.error(res)
            else:
                res.update({'code': 0, 'msg': 'Sign up success'})
                logger.info(res)
            return res
        else:
            res.update({'msg': 'Request action error', 'code': 1013}) #code:1013, no such action when request post /user
            logger.info(res)
            return res

    def delete(self):
        """delete user, with url args:
        1. token, must match username,
        2. username, must match token,
        And, operator must have administrator rights.
        """
        #from pub.config.BLOG import AdminGroup
        AdminGroup = config.BLOG.get('AdminGroup')
        res      = {"url": request.url, "msg": None, "data": None, "code": 200}
        token    = request.args.get('token', None)
        username = request.args.get('username', None)
        if not token:
            res.update({'msg': 'No token', "code": 1020}) #code:1020, 请求参数无token
            logger.warn(res)
            return res
        if not username:
            res.update({'msg': 'No username', "code": 1021}) #code:1021, 请求参数无username
            logger.warn(res)
            return res
        if not username in AdminGroup:
            res.update({'msg': 'The user does not have permission!', "code": 1022}) #code:1022, 请求的username不在配置文件的AdminGroup组，没有删除权限
            logger.error(res)
            return res

        ReqData  = dbUser(username, token=True)
        logger.debug({"User:delete:ReqData": ReqData})
        if ReqData:
            _DBtoken = ReqData.get('token')
            _DBuser  = ReqData.get('username')
            if _DBtoken != token:
                res.update({'msg': 'token miss match!', 'code': 1023}) #code:1023, 请求的token参数与数据库token值不匹配
                logger.error(res)
                return res
            sql = "DELETE FROM user WHERE username='%s'" % username
            logger.info({"User:delete:SQL": sql})
            try:
                if hasattr(mysql, 'delete'):
                    mysql.delete(sql)
                else:
                    mysql.execute(sql)
            except Exception, e:
                res.update({'code':1024, 'msg':'Delete user failed'}) #code:1024, delete user from mysql, it's error
                logger.error(res)
                return res
            else:
                res.update({'code':0, 'msg':'Delete success', 'data':{'delete username': username}}) #token match username, deleter ok
        else:
            res.update({'code': 1025, 'msg':'No found username'}) #code:1025, no such username in mysql.
        logger.info(res)
        return res

    def put(self):
        """Update user profile"""
        pass

