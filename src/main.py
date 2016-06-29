# -*- coding:utf8 -*-

import os
import pub import gen_requestId, logger
from flask import Flask, render_template, g, request

__version__ = '0.1.0'
__date      = '2016-06-29'
__org__     = 'SaintIC'
__author__  = 'Mr.tao <staugur@saintic.com>'
__url__     = 'www.saintic.com'
__doc__     = 'Team Blog Front'

app=Flask(__name__)
app.secret_key = os.urandom(24)

#每个URL请求之前，定义requestId并绑定到g.
@app.before_request
def before_request():
    g.requestId = gen_requestId()
    logger.info("Start Once Access, and this requestId is %s" % g.requestId)

#每次返回数据中，带上响应头，包含API版本和本次请求的requestId，以及允许所有域跨域访问API, 记录访问日志
@app.after_request
def add_header(response):
    response.headers["X-SaintIC-App-Type"] = "Team.Front"
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
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=pub.GLOBAL.get("Debug", True), host=pub.GLOBAL.get("Host", "0.0.0.0"), port=pub.GLOBAL.get("Port", 10050))
