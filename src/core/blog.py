# -*- coding:utf-8 -*-

from pub import logger, mysql
from flask import request
from flask.ext.restful import Resource

class Blog(Resource):

    @classmethod
    def get(self):
        """/blog资源，参数是
        1.num(int, str), 限制列出数据数量，另外可设置为all，列出所有blog。
        2.blogId(int), 列出某一个id的文章, 独立参数。
        3.catalog(bool), 查询博客所有目录，独立参数。
        """

        num    = request.args.get('num')
        blogId = request.args.get('blogId')
        catalog= True if request.args.get("catalog") == "true" or request.args.get("catalog") == "True" else False
        res    = {"url": request.url, "msg": None, "data": None, "code": 0}
        logger.debug({"num": num, "blogId": blogId, "catalog": catalog})

        if catalog:
            sql = "SELECT GROUP_CONCAT(catalog) FROM blog GROUP BY catalog"
            logger.info("SELECT catalog SQL: %s" %sql)
            try:
                data = [ v.split(",")[0] for i in mysql.get(sql) for v in i.values() if v ]
            except Exception,e:
                logger.error(e, exc_info=True)
                data = []
            else:
                res.update(msg = "Catalog query success", data = data)
                logger.info(res)
                return res

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


    def post(self):
        """ 创建博客文章接口:
        :: 1. 验证头部信息
        :: 2. 验证cookie信息
+----+---------+--------------------------+-------------+-------------+--------+-----------+---------+
| id | title   | content                  | create_time | update_time | tag    | catalog   | sources |
+----+---------+--------------------------+-------------+-------------+--------+-----------+---------+
| 47 | 测试1   | 技术博客测试文章         | NULL        | NULL        | 技术   | 未分类    | 原创    |
+----+---------+--------------------------+-------------+-------------+--------+-----------+---------+
        """
        requestId  = request.header.get("requestId")
        requestApp = request.header.get("requestApp")
        #_check_head = 
        sql = "INSERT INTO blog (title,author,time,content,tag,class) VALUES('%s', '%s', '%s', '%s', '%s', '%s')" %(title,author,time,content,tag,classtype)

