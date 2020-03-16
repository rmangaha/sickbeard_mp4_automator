import logging
import os
import sys
from logging.config import fileConfig
try:
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser

defaults = {
    'loggers': {
        'keys': 'root, manual, nzbget',
    },
    'handlers': {
        'keys': 'consoleHandler, nzbgetHandler, fileHandler, manualHandler',
    },
    'formatters': {
        'keys': 'simpleFormatter, minimalFormatter, nzbgetFormatter',
    },
    'logger_root': {
        'level': 'DEBUG',
        'handlers': 'consoleHandler, fileHandler',
    },
    'logger_nzbget': {
        'level': 'DEBUG',
        'handlers': 'nzbgetHandler, fileHandler',
        'propagate': 0,
        'qualname': 'NZBGetPostProcess',
    },
    'logger_manual': {
        'level': 'DEBUG',
        'handlers': 'manualHandler, fileHandler',
        'propagate': 0,
        'qualname': 'MANUAL',
    },
    'handler_consoleHandler': {
        'class': 'StreamHandler',
        'level': 'INFO',
        'formatter': 'simpleFormatter',
        'args': '(sys.stdout,)',
    },
    'handler_nzbgetHandler': {
        'class': 'StreamHandler',
        'level': 'INFO',
        'formatter': 'nzbgetFormatter',
        'args': '(sys.stdout,)',
    },
    'handler_manualHandler': {
        'class': 'StreamHandler',
        'level': 'INFO',
        'formatter': 'minimalFormatter',
        'args': '(sys.stdout,)',
    },
    'handler_fileHandler': {
        'class': 'handlers.RotatingFileHandler',
        'level': 'INFO',
        'formatter': 'simpleFormatter',
        'args': "('%(logfilename)s', 10000, 1)",
    },
    'formatter_simpleFormatter': {
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    },
    'formatter_minimalFormatter': {
        'format': '%(message)s',
        'datefmt': ''
    },
    'formatter_nzbgetFormatter': {
        'format': '[%(levelname)s] %(message)s',
        'datefmt': ''
    }
}


def checkLoggingConfig(configfile):
    write = True
    config = RawConfigParser()
    if os.path.exists(configfile):
        config.read(configfile)
        write = False
    for s in defaults:
        if not config.has_section(s):
            config.add_section(s)
            write = True
        for k in defaults[s]:
            if not config.has_option(s, k):
                config.set(s, k, str(defaults[s][k]))
    if write:
        fp = open(configfile, "w")
        config.write(fp)
        fp.close()


def getLogger(name=None, custompath=None):
    if custompath:
        custompath = os.path.realpath(custompath)
        if not os.path.isdir(custompath):
            custompath = os.path.dirname(custompath)
        rootpath = os.path.abspath(custompath)
        resourcepath = os.path.join(rootpath, "resources")
        configpath = os.path.join(rootpath, "config")
    else:
        resourcepath = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        rootpath = os.path.abspath(os.path.join(resourcepath, "../"))
        configpath = os.path.join(rootpath, "config")

    if os.name == 'nt':
        logpath = configpath
    else:
        logpath = '/var/log'

    if not os.path.isdir(logpath):
        try:
            os.mkdir(logpath)
        except:
            logpath = configpath

    configfile = os.path.abspath(os.path.join(configpath, 'logging.ini')).replace("\\", "\\\\")
    checkLoggingConfig(configfile)

    logfile = os.path.abspath(os.path.join(logpath, 'sma.log')).replace("\\", "\\\\")
    fileConfig(configfile, defaults={'logfilename': logfile})

    return logging.getLogger(name)