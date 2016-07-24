#!/usr/bin/python -O
#product environment start application with `tornado IOLoop` and `gevent server`

from main import app
from pub import logger
from pub.config import GLOBAL, PRODUCT

Host = GLOBAL.get('Host')
Port = GLOBAL.get('Port')
ProcessName = PRODUCT.get('ProcessName')
ProductType = PRODUCT.get('ProductType')

try:
    import setproctitle
except ImportError, e:
    print e
    logger.warn("%s, try to pip install setproctitle, otherwise, you can't use the process to customize the function" %e)
    pass
else:
    setproctitle.setproctitle(ProcessName)
    logger.info("The process is %s" % ProcessName)

try:
    msg = '%s has been launched, %s:%d' %(ProcessName, Host, Port)
    logger.info(msg)
    print msg
    if ProductType == 'gevent':
        from gevent.wsgi import WSGIServer
        http_server = WSGIServer((Host, Port), app)
        http_server.serve_forever()

    elif ProductType == 'tornado':
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(Port)
        IOLoop.instance().start()

    else:
        errmsg='Start the program does not support with %s, abnormal exit!' %ProductType
        logger.error(errmsg)
        raise RuntimeError(errmsg)

except Exception,e:
    print e
    logger.error(e)
