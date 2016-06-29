# -*- coding:utf8 -*-

from log import Syslog

logger        = Syslog.getLogger()
gen_requestId = lambda :str(uuid.uuid4())

