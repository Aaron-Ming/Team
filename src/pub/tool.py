# -*- coding:utf8 -*-

import re
import hashlib
from log import Syslog
import binascii, os, uuid

md5           = lambda pwd:hashlib.md5(pwd).hexdigest()
logger        = Syslog.getLogger()
gen_token     = lambda :binascii.b2a_base64(os.urandom(24))[:32]
gen_requestId = lambda :str(uuid.uuid4())


# 计算加密cookie:
def make_signed_cookie(uid, password, max_age):
    expires = str(int(time.time() + max_age))
    L = [uid, expires, md5('%s-%s-%s-%s' % (uid, password, expires, _COOKIE_KEY))]
    return '-'.join(L)

# 解密cookie:
def parse_signed_cookie(cookie_str):
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        id, expires, md5 = L
        if int(expires) < time.time():
            return None
        user = User.get(id)
        if user is None:
            return None
        if md5 != hashlib.md5('%s-%s-%s-%s' % (id, user.password, expires, _COOKIE_KEY)).hexdigest():
            return None
        return user
    except Exception,e:
        print e
        return None