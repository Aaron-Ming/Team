#-*- coding:utf8 -*-

import json
import requests

__all__ = ["GLOBAL", "MYSQL", "BLOG"]

def getConf():
    url     = "https://api.saintic.com/conf?username=admin&mysql=true"
    headers = {"token": "7h8l4uiKZEopBxjJHGHGduQYLA42Xfbr", 'Content-Type': 'application/json'}
    try:
        _r   = requests.post(url, headers=headers, verify=False)
        data = _r.json()
    except Exception,e:
        from sh import curl
        data = curl("-s", "-L", "-H", "Content-Type: application/json", "-H", "token:%s"%headers.get("token"), "-X", "POST", url)

    if type(data) is dict:
        C3 = data.get("C3")
    else:
        for _j in data:
            C3 = json.loads(_j).get("C3")
            break
    if not isinstance(C3, dict):
        raise TypeError("C3 not dict when access conf api")

    return C3.get("GLOBAL"), C3.get("MYSQL"), C3.get("BLOG")

GLOBAL, MYSQL, BLOG = getConf()
