# -*- coding:utf8 -*-

import os
import json
import time
import uuid
import datetime
from pub import config, gen_requestId, logger, md5
from plugins import session_redis_connect, UserAuth
from flask import Flask, render_template, g, request, redirect, url_for, session, make_response

__version__ = '0.1.0'
__date      = '2016-06-29'
__org__     = 'SaintIC'
__author__  = 'Mr.tao <staugur@saintic.com>'
__url__     = 'www.saintic.com'
__doc__     = 'SaintIC Team Blog Front'

app=Flask(__name__)
app.secret_key = os.urandom(24)
SecretKey = str(uuid.uuid4())

#每个URL请求之前，定义requestId并绑定到g.
@app.before_request
def before_request():
    g.startTime = time.time()
    g.requestId = gen_requestId()
    g.session   = session_redis_connect
    g.auth      = UserAuth()
    g.username  = request.cookies.get("username")
    g.logged_in = request.cookies.get("logged_in")
    g.sessionId = request.cookies.get("sessionId")
    logger.debug("cookie info, username:%s, logged_in:%s, sessionId:%s"%(g.username, g.logged_in, g.sessionId))
    logger.info("Start Once Access, and this requestId is %s" % g.requestId)

#每次返回数据中，带上响应头，包含版本和请求的requestId, 记录访问日志
@app.after_request
def add_header(response):
    response.headers["X-SaintIC-App-Name"] = config.PRODUCT.get("ProcessName", "Team.Front")
    response.headers["X-SaintIC-Request-Id"] = g.requestId
    #response.set_cookie(key="username", value=g.username, expires=datetime.datetime.today() + datetime.timedelta(days=30))
    #response.set_cookie(key="sessionId", value=md5(username + password + SecretKey), expires=datetime.datetime.today() + datetime.timedelta(days=30))
    logger.info(json.dumps({
        "AccessLog": {
            "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            "requestId": g.requestId,
            "OneTimeInterval": "%0.2fs" %float(time.time() - g.startTime),
            "cookies": request.cookies
            }
        }
    ))
    return response

#自定义错误显示信息，404错误和500错误
@app.errorhandler(404)
def not_found(error=None):
    message = 'Not Found: ' + request.url
    return render_template("public/4xx.html", msg=message)

@app.errorhandler(500)
def internal_error(error=None):
    message = 'Internal Server Error: ' + request.url
    return render_template("public/5xx.html", msg=message)

@app.route('/')
def index():
    return render_template('front/index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "GET":
        if session.get("username"):
            return redirect(request.args.get('next', url_for('index')))
        else:
            return render_template("front/login.html", error=error)
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if session.get("username"):
            return redirect(request.args.get('next', url_for('index')))
        else:
            if g.auth.login(username, password) == True:
                ukey = "Team.Front.Session.%s" %username
                expire_time = datetime.datetime.today() + datetime.timedelta(days=30)
                g.session.set(ukey, True)
                session["username"] = True
                logger.info("Add a redis session, key is %s" %ukey)
                resp = make_response(redirect(request.args.get('next', url_for('index'))))
                resp.set_cookie(key='username', value=username, expires=expire_time)
                resp.set_cookie(key='sessionId', value=md5(username + password + SecretKey), expires=expire_time)
                resp.set_cookie(key='logged_in', value="yes", expires=expire_time)
                return resp
            else:
                error = "Login fail, invaild username or password."
                return redirect(url_for("login"))

@app.route('/logout')
def logout():
    try:
        session.pop('username')
    except Exception:
        pass
    return redirect(request.args.get('next', url_for('index')))

@app.route('/uc')
def uc():
    return render_template("uc/home.html", data={})

@app.route('/blog/<int:bid>.html')
def blog(bid):
    return render_template("front/blog.html", blogId=bid)

if __name__ == "__main__":
    from pub.config import GLOBAL
    Host = GLOBAL.get('Host')
    Port = GLOBAL.get('Port')
    Environment = GLOBAL.get("Environment")
    Debug = GLOBAL.get('Debug', True)

    if Environment == "dev":
        app.run(host=Host, port=int(Port), debug=Debug)
    elif Environment == "super debug":
        from werkzeug.contrib.profiler import ProfilerMiddleware
        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [30])
        app.run(debug=Debug, host=Host, port=int(Port))

