# -*- coding:utf-8 -*-

import json
import config
from pub import logger, gen_requestId, gen_token
from flask import Flask, request, g, redirect, jsonify
from flask_restful import Api, Resource

__author__  = 'SaintIC <staugur@saintic.com>'
__doc__     = 'Authentication System for SaintIC Team Project.'
__date__    = '2016-08-04'
__version__ = 'v0.0.1'
__process__ = config.PRODUCT.get('ProcessName', 'Team.Auth')

app = Flask(__name__)
api = Api(app)

#每个URL请求之前，定义requestId并绑定到g.
@app.before_request
def before_request():
    g.requestId = gen_requestId()
    logger.info("Start Once Access, and this requestId is %s" % g.requestId)

#每次返回数据中，带上响应头，包含API版本和本次请求的requestId，以及允许所有域跨域访问API, 记录访问日志
@app.after_request
def add_header(response):
    response.headers["X-SaintIC-Media-Type"] = "saintic." + __version__
    response.headers["X-SaintIC-Request-Id"] = g.requestId
    response.headers["Access-Control-Allow-Origin"] = "*"
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
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


#Define /, make it chcek or get
class Index(Resource):
    def get(self):
        return {
            __process__: "ok"
        }


#Router rules
api.add_resource(Index, '/', endpoint='index')

if __name__ == '__main__':
    from config import GLOBAL
    Host  = GLOBAL.get('Host')
    Port  = GLOBAL.get('Port')
    Debug = GLOBAL.get('Debug', True)
    app.run(host = Host, port = int(Port), debug = Debug)