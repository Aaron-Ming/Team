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

    @classmethod
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
        AppRequestId     = request.header.get("AppRequestId")
        AppRequestName   = request.header.get("AppRequestName")
        AppRequestCookie = request.cookies
        logger.debug(AppRequestCookie)
        AppRequestCookieUsername = request.cookies.get("username", "")
        AppRequestCookiePassword = g.redis.get(Ukey + AppRequestCookieUsername) or ""
        AppRequestCookieSignin   = True if md5(AppRequestCookieUsername + base64.decodestring(AppRequestCookiePassword)) else False

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
        return redirect(url_for('index'))

        sql = "INSERT INTO blog (title,author,time,content,tag,class) VALUES('%s', '%s', '%s', '%s', '%s', '%s')" %(title,author,time,content,tag,classtype)

