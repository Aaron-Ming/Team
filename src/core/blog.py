# -*- coding:utf-8 -*-

from pub import logger, mysql, mysql2, today
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

    @classmethod
    def post(self):
        """ 创建博客文章接口:
        :: 1. 验证头部信息
        :: 2. 验证cookie信息
        """
        AppRequestId     = request.headers.get("AppRequestId")
        AppRequestName   = request.headers.get("AppRequestName")

        logger.debug(request.cookies)

        AppRequestCookieUsername = request.cookies.get("username", "")
        AppRequestCookiePassword = '' # g.redis.get(Ukey + AppRequestCookieUsername) or ""
        AppRequestCookieSignin   = True #if md5(AppRequestCookieUsername + base64.decodestring(AppRequestCookiePassword)) else False
        #get blog form informations.
        blog_title   = request.form.get('title')
        blog_content = request.form.get('content')
        blog_ctime   = today()
        blog_tag     = request.form.get('tag')
        blog_catalog = request.form.get('catalog')
        blog_sources = request.form.get("sources")
        logger.info("blog_title:%s, blog_content:%s, blog_ctime:%s, blog_tag:%s, blog_catalog:%s, blog_sources:%s" %(blog_title, blog_content, blog_ctime, blog_tag, blog_catalog, blog_sources))
        if blog_title and blog_content and blog_ctime and blog_tag and blog_catalog and blog_sources:
            #sql = 'INSERT INTO blog (title,content,create_time,tag,catalog,sources) VALUES ("%s", "%s", "%s", "%s", "%s", "%s")'
            sql = 'INSERT INTO blog (title,content,create_time,tag,catalog,sources) VALUES (%s, %s, %s, %s, %s, %s)'
            logger.info(sql %(blog_title, blog_content, blog_ctime, blog_tag, blog_catalog, blog_sources))
            try:
                blog_id  = mysql2().insert(sql, blog_title, blog_content, blog_ctime, blog_tag, blog_catalog, blog_sources)
            except Exception,e:
                logger.error(e, exc_info=True)
                res = {"code": 3, "data": None, "msg": "blog write error."}
            else:
                res = {"code": 0, "data": blog_id, "msg": "blog write success."}
        else:
            res = {"code": 4, "data": None, "msg": "data form error."}
        logger.info(res)
        return res