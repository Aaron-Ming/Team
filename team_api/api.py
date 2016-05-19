# -*- coding:utf-8 -*-

import re
import json
from pub import logger, mysql, gen_token, gen_requestId
from flask import Flask, request, g, Response, session
from flask.ext.restful import Api, Resource, abort

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
            "status_code": Response.default_status,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            "requestId": g.requestId,
            }
        }
    ))

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
        http_code = Response.default_status
        res={"code": http_code, "url":request_url, "msg": None, "data": None}
        try:
            _num = int(request.args.get('num', 10))
        except ValueError, e:
            logger.warn(e)
            return res.update({"msg": "the num is not integer"})
        else:
            _email = request.args.get('email', None)
            _username = request.args.get('username', None)
            if _username: #username's priority is greater than email
                if request.args.get('token') == 'true':
                    sql="SELECT username,email,cname,motto,url,token,extra FROM user WHERE username=%s LIMIT %d" %(_username, _num)
                else:
                    sql="SELECT username,email,cname,motto,url,extra FROM user WHERE username=%s LIMIT %d" %(_username, _num)
            else:
                if mail.match(_email):
                    if request.args.get('token') == 'true':
                        sql="SELECT username,email,cname,motto,url,token,extra FROM user WHERE email=%s LIMIT %d" %(_email, _num)
                    else:
                        sql="SELECT username,email,cname,motto,url,extra FROM user WHERE email=%s LIMIT %d" %(_email, _num)
                else:
                    res.update({"msg": "mail format error"})
                    logger.info(res)
                    return res
            logger.info({"requestId": g.requestId, "sql": sql})
        try:
            data=mysql.get(sql)
        except Exception,e:
            logger.error(e)
            return res.update({"msg": "get user info error"})
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
api.add_resource(User, '/api/user', '/api/user/', endpoint='api_user')

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
