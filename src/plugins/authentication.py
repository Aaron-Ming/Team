# -*- coding:utf8 -*-

import requests
from pub import logger

class UserAuth:


    def __init__(self):
        self.api = "https://api.saintic.com/user"
        self.headers = {'User-Agent' : 'SaintIC Team Front UserAuth'}
        self.timeout = 3

    def login(self, username, password):
        r = requests.post(self.api, params={"action": "log"}, data={"username": username, "password": password}, headers=self.headers, verify=False, timeout=self.timeout)
        res = r.json()
        logger.info(res)
        if r.status_code == requests.codes.ok:
            res = r.json()
            if "success" in res.get("msg") and res.get('code') == 0:
                return True
        return False

    def registry(self, username, password):
        r = requests.post(self.api, params={"action": "reg"}, data={"username": username, "password": password}, headers=self.headers, verify=False, timeout=self.timeout)
        res = r.json()
        logger.info(res)
        if r.status_code == requests.codes.ok:
            if "success" in res.get("msg") and res.get('code') == 0:
                return True
        return False

    def list(self, **query):
        r = requests.get(self.api, params=query, headers=self.headers, verify=False, timeout=self.timeout)
        res = r.json()
        if "success" in res.get("msg") and res.get("code") == 0:
            return res.get("data")

if __name__ == "__main__":
    user=UserAuth()
    print user.login("admin", "910323")
