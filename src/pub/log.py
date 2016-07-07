#-*- coding:utf8 -*-

import os
import logging.handlers
from config import GLOBAL

loglevel  = GLOBAL.get('LogLevel', "INFO")
CODE_HOME = os.path.dirname(os.path.abspath(__file__))
class Syslog:

    logger = None
    levels = {
        "DEBUG" : logging.DEBUG,
        "INFO" : logging.INFO,
        "WARNING" : logging.WARNING,
        "ERROR" : logging.ERROR,
        "CRITICAL" : logging.CRITICAL}

    log_level = loglevel
    log_dir = os.path.join(os.path.dirname(CODE_HOME), 'logs')
    if not os.path.exists(log_dir): os.mkdir(log_dir)
    log_file = os.path.join(log_dir, 'sys.log')
    #log_max_byte = 10 * 1024 * 1024
    log_max_byte = 1024
    log_backup_count = 5
    log_datefmt = '%Y-%m-%d %H:%M:%S'

    @staticmethod
    def getLogger():
        if Syslog.logger is not None:
            return Syslog.logger

        Syslog.logger = logging.Logger("loggingmodule.Syslog")
        log_handler = logging.handlers.TimedRotatingFileHandler(filename = Syslog.log_file,
                              backupCount = Syslog.log_backup_count,
                              when = "D")
        log_handler.suffix = "%Y%m%d"
        log_fmt = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt=Syslog.log_datefmt)
        log_handler.setFormatter(log_fmt)
        Syslog.logger.addHandler(log_handler)
        Syslog.logger.setLevel(Syslog.levels.get(Syslog.log_level))
        return Syslog.logger

