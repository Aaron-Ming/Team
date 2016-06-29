# -*- coding:utf-8 -*-

from pub import logger, mysql
from flask import request, g
from flask.ext.restful import Resource

class Blog(Resource):

    @classmethod
    def get(self):
        """/blog资源，参数是
        1.num, 限制列出数据数量，默认值10，另外可设置为all，列出所有blog。
        2.id, 列出某一个id的文章。
        """

        num    = request.args.get('num', 10)
        blogId = request.args.get('id')
        code   = 0
        res    = {"url": request.url, "msg": None, 'code': code}

        if not isinstance(blogId, int):
            errmsg = 'blogId not a number'
            logger.warn(errmsg)
            res['msg'] = errmsg
            res['code']= code + 1
            return res
        if num != "all" and not type(num) is int:
            errmsg = 'num not a number or all'
            logger.warn(errmsg)
            res['msg'] = errmsg
            res['code']= code + 2
            return res

        if blogId:
            sql = "SELECT id,title,author,ctime,mtime,content,tag,category FROM blog WHERE id=%d" %blogId  #这条SQL中LIMIT没有意义，省略，所以`num`无意义。
        else:
            if num == "all":
                sql = "SELECT id,title,author,ctime,mtime,content,tag,category FROM blog"
            else:
                sql = "SELECT id,title,author,ctime,mtime,content,tag,category FROM blog LIMIT %d" %num
        try:
            data = mysql.get(sql)
            logger.info({"Blog:get:SQL": sql})
        except Exception,e:
            logger.error(e)
            errmsg = 'get blog error'
            logger.warn(errmsg)
            res['msg'] = errmsg
            res['code']= code + 3
            return res
        else:
            res['msg'] = success
            logger.info(res)
            return res

    def post(self):pass
