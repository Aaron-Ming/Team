"""
#This is public func.
"""

import config
from db import DB
from tool import logger, gen_token, gen_requestId
mysql = DB()

__all__ = ["config", "mysql", "logger", "gen_token", "gen_requestId"]

