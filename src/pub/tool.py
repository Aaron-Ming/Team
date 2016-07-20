# -*- coding:utf8 -*-

from log import Syslog
from uuid import uuid4

md5           = lambda pwd:hashlib.md5(pwd).hexdigest()
logger        = Syslog.getLogger()
gen_requestId = lambda :str(uuid4())
