# -*- coding:utf8 -*-

import hashlib
from log import Syslog
import binascii, os, uuid

md5           = lambda pwd:hashlib.md5(pwd).hexdigest()
logger        = Syslog.getLogger()
gen_token     = lambda :binascii.b2a_base64(os.urandom(24))[:32]
gen_requestId = lambda :str(uuid.uuid4())

if __name__ == "__main__":
    res = {"token": gen_token()}
    res.update({'code': 0})
    logger.debug(res)

