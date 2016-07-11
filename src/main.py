# -*- coding:utf8 -*-

import os
import json
import time
from pub import config, gen_requestId, logger
from plugins import session_redis_connect, UserAuth
from flask import Flask, render_template, g, request

__version__ = '0.1.0'
__date      = '2016-06-29'
__org__     = 'SaintIC'
__author__  = 'Mr.tao <staugur@saintic.com>'
__url__     = 'www.saintic.com'
__doc__     = 'SaintIC Team Blog Front'

app=Flask(__name__)
app.secret_key = os.urandom(24)

#每个URL请求之前，定义requestId并绑定到g.
@app.before_request
def before_request():
    g.startTime = time.time()
    g.requestId = gen_requestId()
    g.session   = session_redis_connect
    g.user      = UserAuth()
    logger.info("Start Once Access, and this requestId is %s" % g.requestId)

#每次返回数据中，带上响应头，包含版本和请求的requestId, 记录访问日志
@app.after_request
def add_header(response):
    response.headers["X-SaintIC-App-Name"] = config.PRODUCT.get("ProcessName", "Team.Front")
    response.headers["X-SaintIC-Request-Id"] = g.requestId
    logger.info(json.dumps({
        "AccessLog": {
            "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            "requestId": g.requestId,
            "OneTimeInterval": "%0.2fs" %float(time.time() - g.startTime)
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
    username = _user = ""
    if request.method == "GET":
        #session rule is session_`username`
        #username = g.user.get("name", None)
        if username and g.session.get(username):
            return redirect(request.args.get('next') or url_for('index'))
        else:
            return render_template("front/login.html", error=error)
    if request.method == "POST":
        _user = request.form.get("username")
        _pass = request.form.get("password")
        if g.user.login(_user, _pass) == True:
            _ukey = "session_%s" %_user
            g.session.set(_ukey, True)
            logger.info("Add a session, key is %s" %_ukey)
        else:
            error = "Login fail, invaild username or password."
        redirect(url_for("login"))

@app.route('/uc')
def uc():
    return render_template("uc/home.html", data={})

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

