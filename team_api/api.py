# -*- coding:utf-8 -*-

import re
import json
from pub import logger, mysql, gen_token, gen_requestId
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

class Index(Resource):
    def get(self):
        return {"Team Api": "Welcome %s" %request.headers.get('X-Real-Ip', request.remote_addr)}

class User(Resource):

    def get(self):
        """Public func, no token, with url args:
        1. num, 展现的数量,
        2. username|email, 用户名或邮箱，数据库主键，唯一.

        返回数据样例，{'msg':'success or error(errmsg)', 'code':'http code', 'data':data, 'url':request_url}
        """
        request_url = request.url
        http_code = "200 ok"
        res={"code": http_code, "url":request_url, "msg": None, "data": None}
        logger.debug({"default_response": res, "requestId": str(g.requestId)})
        try:
            _num = int(request.args.get('num', 10))
        except ValueError, e:
            logger.warn(e)
            return res.update({"msg": "the num is not integer"})
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
            #try...except...else(if...elif...else) end, write log sql and requestId
            logger.info({"requestId": g.requestId, "User Get End SQL": sql})
        try:
            data=mysql.get(sql)
        except Exception,e:
            logger.error(e)
            return res.update({"msg": "get user info error"})
        else:
            res.update({"msg": "success", "data": data})
        logger.info(res)
        return res

    def post(self):
        if True:
            username = request.form.get('username', None)
            password = request.form.get('password', None)
            email    = request.form.get('email', 'NULL')
            extra    = request.form.get('extra', 'NULL')
        if username == None or password == None:
            abort(400, message="username or password is empty!")
        if re.match(r'([0-9a-zA-Z\_*\.*\-*]+)@([a-zA-Z0-9\-*\_*\.*]+)\.([a-zA-Z]+$)', email) == None:
            abort(400, message="email format error")
        sql = "select username from user where username='%s'" % username
        logger.info(sql)
        if mysql.select(sql):
            data = {'code':1024, 'msg':'User already exists'}
            logger.warn(data)
        else:
            sql = "insert into user (username, password, email, extra) values('%s', '%s', '%s', '%s')" % (username, md5(password), email, extra)
            try:
                if hasattr(mysql, 'insert'):
                    mysql.insert(sql)
                else:
                    mysql.execute(sql)
                logger.info(sql)
            except Exception, e:
                data = {'code':1025, 'msg':'Sign up failed'}
                logger.error(data)
            else:
                data = {'code':0, 'msg':'Sign up success', 'data':{'username':username, 'email':email}}
                logger.info(data)
        return data

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
