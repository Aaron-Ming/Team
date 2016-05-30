# -*- coding:utf-8 -*-

import json
from pub import logger, gen_requestId
from flask import Flask, request, g, redirect, jsonify, Response
from flask.ext.restful import Api, Resource
from core import (User, Blog, Token)

__author__  = 'SaintIC <staugur@saintic.com>'
__doc__     = "Team Blog Api System for SaintIC, the GitHub URL is https://github.com/saintic/Team, now branch is api."
__date__    = '2016-05-19'
__version__ = '1.0.0'
__version_list__ = [ _v for _v in __version__ if _v != '.' ]

app  = Flask(__name__)
api  = Api(app)

#每个URL请求之前，定义requestId并绑定到g，JSON化写入日志中。
@app.before_request
def before_request():
    g.requestId = gen_requestId()
    logger.info(json.dumps({
        "AccessLog": {
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

#每次返回数据中，带上响应头，包含API版本和本次请求的requestId，以及允许所有域跨域访问API.
@app.after_request
def add_header(response):
    response.headers["X-SaintIC-Media-Type"] = "saintic.v" + __version_list__[0]
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

#Define /, make it chcek or get
class Index(Resource):
    def get(self):
        return {"Team.Api": "Welcome %s" %request.headers.get('X-Real-Ip', request.remote_addr)}

@app.route('/favicon.ico')
def favicon():
    return redirect("https://www.saintic.com/static/images/favicon.ico")

#Router rules
api.add_resource(Index, '/', endpoint='index')
api.add_resource(User, '/user', '/user/', endpoint='user')
api.add_resource(Token, '/token', '/token/', endpoint='token')
api.add_resource(Blog, '/blog', '/blog/', endpoint='blog')

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
