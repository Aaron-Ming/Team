# -*- coding:utf8 -*-

from log import Syslog
import binascii, os, uuid

logger        = Syslog.getLogger()
gen_token     = lambda :binascii.b2a_base64(os.urandom(24))[:32]
gen_requestId = lambda :str(uuid.uuid4())

if __name__ == "__main__":
    print gen_requestId()
