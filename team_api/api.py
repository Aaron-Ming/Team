# -*- coding:utf-8 -*-

import re
import json
from pub import logger, mysql, gen_token, gen_requestId, md5
from flask import Flask, request, g, jsonify, session, make_response, Response
from flask.ext.restful import Api, Resource, abort

__version__ = '1.0.0'
__version_list__ = [ _v for _v in __version__ if _v != '.' ]
__author__ = 'SaintIC <staugur@saintic.com>'
__date__ = '2016-05-19'
__doc__ = "Team Blog System for SaintIC, the GitHub URL is https://github.com/saintic/Team, now branch is api."

app = Flask(__name__)
api = Api(app)
mail= re.compile(r'([0-9a-zA-Z\_*\.*\-*]+)@([a-zA-Z0-9\-*\_*\.*]+)\.([a-zA-Z]+$)')

#每个URL请求之前，定义requestId并绑定到g，并序列化写入日志中。
@app.before_request
def before_request():
    g.requestId = gen_requestId()
    logger.info(json.dumps({
        "AccessLog": {
            "login_user": session.get('username', None),
            "status_code": str(Response.status_code),
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            "requestId": str(g.requestId),
            }
        }
    ))

#每次返回数据中，带上响应头，包含API版本和本次请求的ID，以及允许所有域跨域访问API.
@app.after_request
def add_header(response):
    response.headers["X-SaintIC-Media-Type"] = "saintic.v"+__version_list__[0]
    response.headers["X-SaintIC-Request-Id"] = str(g.requestId)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

#自定义错误显示信息，404错误和500错误
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.errorhandler(500)
def internal_error(error=None):
    message = {
        'status': 500,
        'message': 'Internal Server Error: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 500
    return resp

#API所需要的公共函数
def dbUser(username=None, password=False):
    "获取数据库中所有用户或是否存在某个具体用户(方法: username=username)"
    if username:
        if password == True:
            sql = "SELECT username,password FROM user WHERE username='%s'" % username
        else:
            sql = "SELECT username FROM user WHERE username='%s'" % username
    else:
        #All user from mysql(team.user)
        sql = "SELECT username FROM user"
    logger.info({"func:dbUser:sql":sql})
    try:
        data = mysql.get(sql)
    except Exception, e:
        logger.error({"func:dbUser:exec_sql":sql})
        return None
    else:
        return data

#Define /, make it chcek or get
class Index(Resource):
    def get(self):
        return {"Team.Api": "Welcome %s" %request.headers.get('X-Real-Ip', request.remote_addr)}

class User(Resource):
    """User resource, url is /user, /user/.
    1. #get:    Get user
    2. #post:   Create user, registry and login
    3. #put:    Update user profile
    4. #delete: Delete user
    """
    def get(self):
        """Public func, no token, with url args:
        1. num, 展现的数量,
        2. username|email, 用户名或邮箱，数据库主键，唯一.

        返回数据样例，{'msg':'success or error(errmsg)', 'code':'http code', 'data':data, 'url':request_url}
        """
        request_url = request.url
        http_code = "200 ok"
        res={"code": http_code, "url":request_url, "msg": None, "data": None}
        try:
            _num = int(request.args.get('num', 10))
        except ValueError, e:
            logger.warn(e)
            res.update({"msg": "the num is not integer"})
            return res
        else:
            _email = request.args.get('email', None)
            _username = request.args.get('username', None)
            _token = request.args.get('token')
            logger.debug({"email":_email, "username":_username, "token":_token, "requestId": str(g.requestId)})
            if _username: #username's priority is greater than email
                if _token == 'true':
                    sql="SELECT username,email,cname,motto,url,token,extra FROM user WHERE username='%s' LIMIT %d" %(_username, _num)
                else:
                    sql="SELECT username,email,cname,motto,url,extra FROM user WHERE username='%s' LIMIT %d" %(_username, _num)
            elif _email:
                emails=mysql.get("SELECT email FROM user")
                logger.debug({"first email": emails, "requestId": str(g.requestId)})
                emails=[ email.email for email in emails if email.email ]
                logger.debug({"second email":emails, "requestId": str(g.requestId)})
                if not _email in emails: #check email in mysql
                    res.update({"msg": "no such email"})
                    logger.info(res)
                    return res
                if mail.match(_email):
                    if _token == 'true':
                        sql="SELECT username,email,cname,motto,url,token,extra FROM user WHERE email='%s' LIMIT %d" %(_email, _num)
                    else:
                        sql="SELECT username,email,cname,motto,url,extra FROM user WHERE email='%s' LIMIT %d" %(_email, _num)
                else:
                    res.update({"msg": "mail format error"})
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
            res.update({"msg": "get user info error"})
            return res
        else:
            res.update({"msg": "success", "data": data})
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
        request_url = request.url
        res = {"url": request_url, "msg": None, "data": None}
        try:
            username = request.json.get('username', None)
            password = request.json.get('password', None)
            email    = request.json.get('email')
        except Exception, e:
            logger.error(e)
            res.update({'msg': 'no username or password'})
            return res
        else:
            res.update({'data': {'username': username, 'email': email}})
        if not username or not password:
            logger.debug({"User:post:request.json": (username, password), "res": res.update({'msg': 'Invaild username or password'})})
            return res
        if email and re.match(r'([0-9a-zA-Z\_*\.*\-*]+)@([a-zA-Z0-9\-*\_*\.*]+)\.([a-zA-Z]+$)', email) == None:
            logger.debug({"User:post:request.json": email, "res": res.update({'msg': "email format error"})})  #when email has set, otherwise, pass `if...abort`
            return res
        #Start Action with (log, reg)
        action = request.args.get("action") #log or reg (登录or注册)
        ReqData = dbUser(username, password=True)
        logger.debug({"request.type": action, 'ReqData': ReqData})
        _MD5pass = md5(password)
        if action == 'log':
            _DBuser  = ReqData.get('username')
            _DBpass  = ReqData.get('password')
            if not ReqData:
                res.update({'msg':'User not exists'})
                logger.warn(res)
                return res
            #ReqData is True(user is exists), it's dict, eg:{'username': u'xxxxx', 'password': u'xxxxxxxxxx'}
            logger.debug({'ReqUser': username, 'ReqPassMD5': _MD5pass, 'DBuser': _DBuser, 'DBpass': _DBpass})
            if len(username) < 5:
                res.update({'msg': 'Username length of at least 5', 'code': 1010}) #code:1010, username length < 5
                logger.warn(res)
                return res
            if _MD5pass == _DBpass:
                res.update({'msg': 'Verify Success', 'code': 0}) #code:0, it's successful
            else:
                res.update({'msg': 'Verify Fail', 'code': 1011}) #code:1011, request pass != mysql pass
            logger.info(res)
            return res
        elif action == 'reg':
            sql = "INSERT INTO user (username, password, email) VALUES('%s', '%s', '%s')" % (username, _MD5pass, email)
            if ReqData:
                res.update({'msg': 'User already exists, cannot be registered!'})
                logger.warn(res)
                return res
            try:
                if hasattr(mysql, 'insert'):
                    mysql.insert(sql)
                else:
                    mysql.execute(sql)
                logger.info({"User:post:reg:sql": sql})
            except Exception, e:
                res.update({'code':1026, 'msg':'Sign up failed'}) #code:1026, sign up failed when write into mysql
                logger.error(res)
            else:
                res.update({'code': 0, 'msg': 'Sign up success'})
                logger.info(res)
            return res
        else:
            res.update({'msg': 'Request action error', 'code': 1025}) #code:1025, no such action when request post /user
            logger.info(res)
            return res

    def delete(self):
        pass

    def put(self):
        pass

api.add_resource(Index, '/', endpoint='index')
#api.add_resource(Blog, '/api/blog', '/api/blog/', endpoint='api_blog')
api.add_resource(User, '/user', '/user/', endpoint='user')

if __name__ == '__main__':
    from pub.config import GLOBAL
    Host = GLOBAL.get('Host')
    Port = GLOBAL.get('Port')
    Environment = GLOBAL.get('Environment')
    Debug = GLOBAL.get('Debug', True)

    if Environment == "dev":
        app.run(host=Host, port=int(Port), debug=Debug)
    elif Environment == "super debug":
        from werkzeug.contrib.profiler import ProfilerMiddleware
        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [30])
        app.run(debug=Debug, host=Host, port=int(Port))
