# coding:utf8
from main import app
from pub.config import GLOBAL
from werkzeug.contrib.profiler import ProfilerMiddleware
Host = GLOBAL.get('Host')
Port = GLOBAL.get('Port')
app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [30])
app.run(debug=True, host=Host, port=int(Port))