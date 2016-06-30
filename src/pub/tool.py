# -*- coding:utf8 -*-

from log import Syslog
from uuid import uuid4

logger        = Syslog.getLogger()
gen_requestId = lambda :str(uuid4())

