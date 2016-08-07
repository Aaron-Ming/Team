# -*- coding:utf8 -*-

import os
import json
import time
import base64
from pub import config, gen_requestId, logger, md5, Uploader
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
    g.refererUrl= request.cookies.get("Url") if request.cookies.get("Url") and not "/auth" in request.cookies.get("Url") and not "favicon.ico" in request.cookies.get("Url") and not "robots.txt" in request.cookies.get("Url") and not "/logout" in request.cookies.get("Url") and not "index.js.map" in request.cookies.get("Url") and not "static" in request.cookies.get("Url") else url_for("index")
    logger.info("Start Once Access, and this requestId is %s, refererUrl is %s" %(g.requestId, g.refererUrl))
    g.redis     = session_redis_connect
    g.auth      = UserAuth()
    g.username  = request.cookies.get("username", "")
    g.sessionId = request.cookies.get("sessionId")
    g.password  = g.redis.get(Ukey + g.username) if g.redis.get(Ukey + g.username) else ""
    g.signin    = True if g.sessionId == md5(g.username + base64.decodestring(g.password)) else False
    logger.debug("Cookie debug, username:%s, sessionId:%s, signin:%s"%(g.username, g.sessionId, g.signin))

#每次返回数据中，带上响应头，包含版本和请求的requestId, 记录访问日志
@app.after_request
def add_header(response):
    response.headers["X-SaintIC-App-Name"] = config.PRODUCT.get("ProcessName", "Team.Front")
    response.headers["X-SaintIC-Request-Id"] = g.requestId
    response.set_cookie(key="Url", value=request.url, expires=None)
    logger.info(json.dumps({
        "AccessLog": {
            "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "Url": request.url,
            "referer": request.headers.get('Referer') or g.refererUrl,
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

@app.route('/robots.txt')
def robots():
    return render_template('public/robots.txt')

@app.route('/uc/<username>/')
def uc(username):
    if g.signin:
        return render_template("uc/home.html", username=username)
    else:
        return redirect(url_for('login'))

@app.route('/blog/<int:bid>.html')
def blog(bid):
    import requests
    #data=requests.get("https://api.saintic.com/blog?blogId="+str(bid), timeout=3).json()
    #return render_template("front/new-blog.html", title=data['data'].get("title"), data=data['data'].get("content"))
    return render_template("front/blog.html", blogId=bid)

@app.route('/login/', methods=["GET", "POST"])
def login():
    if g.signin:
        return redirect(request.args.get('next', g.refererUrl))
    else:
        return render_template("front/login.html")

@app.route('/auth/', methods=["POST"])
def auth():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    try:
        if g.signin:
            return redirect(request.args.get('next', g.refererUrl))
        elif g.auth.login(username, password) == True:
            key = Ukey + username
            #expire_time = datetime.datetime.today() + datetime.timedelta(days=30)
            #resp = make_response(redirect(request.args.get('next', g.refererUrl)))
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

@app.route('/logout/')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie(key='logged_in', value='', expires=0)
    resp.set_cookie(key='username',  value='', expires=0)
    resp.set_cookie(key='sessionId',  value='', expires=0)
    return resp


#博客创建页面
@app.route('/blog/create/', methods = ["GET", "POST"])
def blog_create_page():
    if g.signin:
        if request.method == "GET":
            return render_template("front/blog_create.html")
        if request.method == "POST":
            title     = request.form.get('title')
            author    = username
            time      = today()
            content   = request.form.get(u'editor')
            if content.find('\'') >= 0: content = content.replace('\'', '\"')
            tag       = request.form.get('tag')
            classtype = request.form.get('type')
            logger.debug(type(content))
            sql = u"INSERT INTO blog (title,author,time,content,tag,class) VALUES('%s', '%s', '%s', '%s', '%s', '%s')" %(title,author,time,content,tag,classtype)
            #sql="INSERT INTO blog(title,author,time,content,tag,class) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(title,author,time,content,tag,classtype)
            logger.debug({'title': title})
            logger.debug({'time': time})
            logger.debug({'author': author})
            logger.debug({'content': content.find('\'')})
            logger.info(sql)
            #此处需要重写DB类的insert方法，用(sql, arg1, arg2, ...)插入数据库中避免错误
            try:
                mysql.execute(sql)
            except Exception,e:
                logger.error(e)
            return redirect(url_for('create_blog'))
        return render_template('user/blog-new.html', username=username, data=userdata, types=ClassData())
    else:
        return redirect(url_for('login'))

@app.route('/home/upload/', methods=['GET', 'POST', 'OPTIONS'])
def upload():
    """UEditor文件上传接口

    config 配置文件
    result 返回结果
    """
    mimetype = 'application/json'
    result = {}
    action = request.args.get('action')

    # 解析JSON格式的配置文件
    with open(os.path.join(app.static_folder, 'ueditor', 'php',
                           'config.json')) as fp:
        try:
            # 删除 `/**/` 之间的注释
            CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
        except:
            CONFIG = {}

    if action == 'config':
        # 初始化时，返回配置文件给客户端
        result = CONFIG

    elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
        # 图片、文件、视频上传
        if action == 'uploadimage':
            fieldName = CONFIG.get('imageFieldName')
            config = {
                "pathFormat": CONFIG['imagePathFormat'],
                "maxSize": CONFIG['imageMaxSize'],
                "allowFiles": CONFIG['imageAllowFiles']
            }
        elif action == 'uploadvideo':
            fieldName = CONFIG.get('videoFieldName')
            config = {
                "pathFormat": CONFIG['videoPathFormat'],
                "maxSize": CONFIG['videoMaxSize'],
                "allowFiles": CONFIG['videoAllowFiles']
            }
        else:
            fieldName = CONFIG.get('fileFieldName')
            config = {
                "pathFormat": CONFIG['filePathFormat'],
                "maxSize": CONFIG['fileMaxSize'],
                "allowFiles": CONFIG['fileAllowFiles']
            }

        if fieldName in request.files:
            field = request.files[fieldName]
            uploader = Uploader(field, config, app.static_folder)
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'

    elif action in ('uploadscrawl'):
        # 涂鸦上传
        fieldName = CONFIG.get('scrawlFieldName')
        config = {
            "pathFormat": CONFIG.get('scrawlPathFormat'),
            "maxSize": CONFIG.get('scrawlMaxSize'),
            "allowFiles": CONFIG.get('scrawlAllowFiles'),
            "oriName": "scrawl.png"
        }
        if fieldName in request.form:
            field = request.form[fieldName]
            uploader = Uploader(field, config, app.static_folder, 'base64')
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'

    elif action in ('catchimage'):
        config = {
            "pathFormat": CONFIG['catcherPathFormat'],
            "maxSize": CONFIG['catcherMaxSize'],
            "allowFiles": CONFIG['catcherAllowFiles'],
            "oriName": "remote.png"
        }
        fieldName = CONFIG['catcherFieldName']

        if fieldName in request.form:
            # 这里比较奇怪，远程抓图提交的表单名称不是这个
            source = []
        elif '%s[]' % fieldName in request.form:
            # 而是这个
            source = request.form.getlist('%s[]' % fieldName)

        _list = []
        for imgurl in source:
            uploader = Uploader(imgurl, config, app.static_folder, 'remote')
            info = uploader.getFileInfo()
            _list.append({
                'state': info['state'],
                'url': info['url'],
                'original': info['original'],
                'source': imgurl,
            })

        result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
        result['list'] = _list

    else:
        result['state'] = '请求地址出错'

    result = json.dumps(result)

    if 'callback' in request.args:
        callback = request.args.get('callback')
        if re.match(r'^[\w_]+$', callback):
            result = '%s(%s)' % (callback, result)
            mimetype = 'application/javascript'
        else:
            result = json.dumps({'state': 'callback参数不合法'})

    res = make_response(result)
    res.mimetype = mimetype
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return res

if __name__ == "__main__":
    from pub.config import GLOBAL
    Host = GLOBAL.get('Host')
    Port = GLOBAL.get('Port')
    Debug = GLOBAL.get('Debug', True)
    app.run(host=Host, port=int(Port), debug=Debug)
