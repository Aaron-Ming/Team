# -*- coding:utf8 -*-

import pub
from flask import Flask, render_template, g

__version__ = '1.0'
__date      = '2016-06-13'
__author__  = 'SaintIC'
__url__     = 'www.saintic.com'
__doc__     = 'Team Project Front'

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=pub.GLOBAL.get("Debug", True), host=pub.GLOBAL.get("Host", "0.0.0.0"), port=pub.GLOBAL.get("Port", 10050))
