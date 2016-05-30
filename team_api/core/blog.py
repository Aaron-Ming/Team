# -*- coding:utf-8 -*-

from pub import logger, mysql
from flask import request, g
from flask.ext.restful import Resource

class Blog(Resource):
    def get(self):
        try:
            num = int(request.args.get('num', 10))
        except ValueError,e:
            logger.warn(e)
            return {"code":126, "msg": "num is not integer"}
        #num, 限制列出数据数量，默认值10，不参与优先级
        listBlogId = request.args.get('list', False) #列出博客所有id，优先级1
        id = request.args.get('id', None)           #查看某个id的博客数据，优先级2
        if id != None:
            try:
                id=int(id)
            except ValueError,e:
                logger.debug(type(id)+id)
                return {"code":126, "msg": "id is invaild"}

        if listBlogId == True or listBlogId == 'true':
            sql="SELECT id FROM blog LIMIT %d" %num
        else:
            if id:
                sql="SELECT * FROM blog WHERE id='%s'" % id
            else:
                sql="SELECT * FROM blog LIMIT %d" % num
        try:
            data=mysql.get(sql)
            logger.info(sql)
            code=0
        except Exception,e:
            logger.error(e)
            code=127
        _result={'code':code, 'msg':'Get Blogs', 'data':data}
        logger.info(_result)
        return _result


