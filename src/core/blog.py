# -*- coding:utf-8 -*-

from pub import logger, mysql
from flask import request
from flask.ext.restful import Resource

class Blog(Resource):

    @classmethod
    def get(self):
        """/blog资源，参数是
        1.num, 限制列出数据数量，默认值10，另外可设置为all，列出所有blog。
        2.id, 列出某一个id的文章,优先级最高。
        """

        num    = request.args.get('num', 10)
        blogId = request.args.get('blogId', None)
        res    = {"url": request.url, "msg": None, "data": None, "code": 0}

        if blogId:
            sql = "SELECT id,title,content,create_time,update_time,tag,catalog,sources FROM blog WHERE id=%s" %blogId
        else:
            if num == "all":
                sql = "SELECT id,title,content,create_time,update_time,tag,catalog,sources FROM blog"
            else:
                if isinstance(num, int):
                    sql = "SELECT id,title,content,create_time,update_time,tag,catalog,sources FROM blog LIMIT %d" %num
                else:
                    res.update(msg = 'num not a integer or all, or no blogId query.', code = 1)
                    logger.warn(res)
                    return res
        try:
            data = mysql.get(sql)
            logger.info({"Blog:get:SQL": sql})
        except Exception,e:
            logger.error(e, exc_info=True)
            res.update(msg = "get blog error", code = 2)
            logger.info(res)
            return res
        else:
            res.update(msg = 'success', data = data)
            logger.info(res)
            return res

    def post(self):pass
