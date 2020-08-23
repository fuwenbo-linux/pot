'''
  简单得实时更新日志记录文件
'''

import logging
from logging.handlers import TimedRotatingFileHandler
# create logger with 'spam_application'
logger = logging.getLogger('study and test')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
#fh = logging.FileHandler('myapp.log')
#fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
#保存时间备份按照秒来计算
th = TimedRotatingFileHandler(filename="myapp1.log",backupCount=5,when="h")
th.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
th.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)
logger.addHandler(th)

logger.info("hello12!")
