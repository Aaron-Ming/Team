# -*- coding:utf-8 -*-

from pub import logger, mysql, dbUser, md5, gen_token
from flask import request, g
from flask.ext.restful import Resource

class Token(Resource):
    def post(self):
        """create token, with post data:
        1. username,
        2. password,
        return token
        """
        code= 1030
        res = {"url": request.url, "msg": None, 'code': code}
        logger.debug("Token:post:request.json is %s"%request.json)
        if request.json: #header ask: "Content-type: application/json"
            username = request.json.get('username', None)
            password = request.json.get('password', None)
        else:            #this is default form ask
            logger.debug("No request.json, start request.form")
            logger.error({"request.json.data": request.json, "request.json.type": type(request.json), "message": "No request.json, return"})
            try:
                username = request.form.get('username', None)
                password = request.form.get('password', None)
            except Exception, e:
                logger.error(e)
                res['msg'] = 'No username or password in request, you maybe set headers with "Content-Type: application/json" next time.'
                res['code']= code + 1
                return res 
        #login check(as a function), in user.py(User:post:action=log)
        ReqData = dbUser(username, password=True, token=True)
        if not ReqData:
            res['msg'] = 'User not exists'
            res['code']= code + 2
            logger.warn(res)
            return res
        #ReqData is True(user is exists), it's dict, eg:{'username': u'xxxxx', 'password': u'xxxxxxxxxx'}
        _Reqpass = md5(password)
        _DBuser  = ReqData.get('username')
        _DBpass  = ReqData.get('password')
        _DBtoken = ReqData.get('token')
        if _DBtoken:
            res.update({'msg': 'Token already exists', 'code': code + 3, "token": _DBtoken})
            logger.warn(res)
            return res
        if _Reqpass == _DBpass:
            token = gen_token()
            res.update({'msg': 'username + password authentication success, token has been created.', 'code': 0, 'token': token})
            sql = "UPDATE user SET token='%s' WHERE username='%s'" % (token, username)
            try:
                mysql.update(sql)
                logger.info('Token:post:create_token:sql--> "%s"' %sql)
            except Exception,e:
                logger.error(e)
                res['msg'] = 'token insert error' #had token for return
                return res
        else:
            res.update({'msg': 'username + password authentication failed', 'code': code + 4})
        logger.info(res)
        return res
