# -*- coding:utf8 -*-

import os
import json
import time
import base64
from pub import config, gen_requestId, logger, md5
from plugins import session_redis_connect, UserAuth
from flask import Flask, render_template, g, request, redirect, url_for, make_response, jsonify

__version__ = '0.1.0'
__date      = '2016-06-29'
__org__     = 'SaintIC'
__author__  = 'Mr.tao <staugur@saintic.com>'
__url__     = 'www.saintic.com'
__doc__     = 'SaintIC Team Blog Front'

app=Flask(__name__)
app.secret_key = os.urandom(24)
Ukey = "Team.Front.Session."

#每个URL请求之前，定义requestId并绑定到g.
@app.before_request
def before_request():
    g.startTime = time.time()
    g.requestId = gen_requestId()
    g.redis     = session_redis_connect
    g.auth      = UserAuth()
    g.username  = request.cookies.get("username", "")
    g.sessionId = request.cookies.get("sessionId")
    g.password  = g.redis.get(Ukey + g.username) if g.redis.get(Ukey + g.username) else ""
    g.signin    = True if g.sessionId == md5(g.username + base64.decodestring(g.password)) else False
    logger.info("Start Once Access, and this requestId is %s" % g.requestId)
    logger.debug("Cookie debug, username:%s, sessionId:%s, signin:%s"%(g.username, g.sessionId, g.signin))

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

@app.route('/')
def index():
    return render_template('front/index.html')

@app.route('/uc/<username>')
def uc(username):
    if g.signin:
        return render_template("uc/home.html", username=username)
    else:
        return redirect(url_for('login'))

@app.route('/blog/<int:bid>.html')
def blog(bid):
    return render_template("front/blog.html", blogId=bid)

@app.route('/login', methods=["GET", "POST"])
def login():
    if g.signin:
        return redirect(request.args.get('next', url_for('index')))
    else:
        return render_template("front/login.html")

@app.route('/auth', methods=["POST"])
def auth():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    try:
        if g.signin:
            return redirect(request.args.get('next', url_for('index')))
        elif g.auth.login(username, password) == True:
            key = Ukey + username
            #expire_time = datetime.datetime.today() + datetime.timedelta(days=30)
            #resp = make_response(redirect(request.args.get('next', url_for('index'))))
            if g.redis.set(key, base64.encodestring(password)):
                logger.info("Create a redis session key(%s) successfully." %key)
                resp = jsonify(loggedIn=True)
                resp.set_cookie(key='logged_in', value="yes", expires=None)
                resp.set_cookie(key='username',  value=username, expires=None)
                resp.set_cookie(key='sessionId', value=md5(username + password), expires=None)
            else:
                resp = jsonify(loggedIn=False)
                logger.warn("Create a redis session key(%s) failed." %key)
            return resp
        else:
            error = "Login fail, invaild username or password."
            logger.debug(error)
            return jsonify(loggedIn=False, error=error)
    except Exception,e:
        logger.error(e, exc_info=True)
        return jsonify(loggedIn=False, error="Server Exception")

@app.route('/logout')
def logout():
    resp = make_response(redirect(request.args.get('next', url_for('index'))))
    resp.set_cookie(key='logged_in', value='', expires=0)
    resp.set_cookie(key='username',  value='', expires=0)
    resp.set_cookie(key='sessionId',  value='', expires=0)
    return resp

if __name__ == "__main__":
    from pub.config import GLOBAL
    Host = GLOBAL.get('Host')
    Port = GLOBAL.get('Port')
    Debug = GLOBAL.get('Debug', True)
    app.run(host=Host, port=int(Port), debug=Debug)