import logging
from logging.handlers import RotatingFileHandler
# create logger with 'spam_application'
def getLogger(name,filename):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    #fh = logging.FileHandler('myapp.log')
    #fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    rh = RotatingFileHandler(filename=filename,maxBytes=10*1024*1024, backupCount=5)
    rh.setLevel(logging.WARNING)
    #保存时间备份按照秒来计算
    #th = TimedRotatingFileHandler(filename=filename,backupCount=5,when="h")
    #th.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    rh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)
    logger.addHandler(rh)
    return logger