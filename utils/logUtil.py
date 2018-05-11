# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 12:42:05 2018

@author: dell
"""

import math
import logging
#import sys
from functools import wraps
import time,os,stat
# 创建一个logger，用来管理输出文件路径   
logger = logging.getLogger('mylogger')   
logger.setLevel(logging.DEBUG)   
     
# 创建一个handler，用于写入日志文件   
fh = logging.FileHandler('test.log')   
fh.setLevel(logging.DEBUG)   
     
# 再创建一个handler，用于输出到控制台   
ch = logging.StreamHandler()   
ch.setLevel(logging.DEBUG)   
     
# 定义handler的输出格式
formatter = logging.Formatter('[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')  
fh.setFormatter(formatter)   
ch.setFormatter(formatter)   
     
# 给logger添加handler   
logger.addHandler(fh)   
logger.addHandler(ch)   
     
class util:
    def getFloorTimestamp(timestamp):
        return math.floor((timestamp+8*60*60)/60/60/24)*60*60*24-8*60*60
    
    def getCeilTimestamp(timestamp):
        return math.ceil((timestamp+8*60*60)/60/60/24)*60*60*24-8*60*60
    
    def logger(func):
        """
            self, 为filehandler，event为handler处理的事件类型
            修正由于在handler中继承的方法中move方法的存在，在对move方法
            装饰的时候，会出现 os.stat(filepath) path不存在的情况就是src_path
            如果不处理会引发错误停止观察期的watch功能
        """
        @wraps(func)
        def wrapper(self,event):
            try:
                filepath = event.src_path
                fileStats = os.stat(filepath)   
                fileInfo = {  
                    'Size':fileStats [ stat.ST_SIZE ],                         #获取文件大小  
                    'LastModified':time.ctime( fileStats [ stat.ST_MTIME ] ),  #获取文件最后修改时间  
                    'LastAccessed':time.ctime( fileStats [ stat.ST_ATIME ] ),  #获取文件最后访问时间  
                    'CreationTime':time.ctime( fileStats [ stat.ST_CTIME ] ),  #获取文件创建时间  
                    'Mode':fileStats [ stat.ST_MODE ],                          #获取文件的模式  
                    'Path': event.src_path,   #事件发生地址或文件路径
                    'EventType': event.event_type,
                    'is_dir':event.is_directory,
                    'id':id(event)
                }
                
                logger.info(fileInfo)
            except FileNotFoundError:
                logger.error("Can not found the filename:"+event.src_path+ \
                             "\nEventType:"+str(type(event)))
            finally:
                func(self,event)
        return wrapper

##方法2 打印到前台
#console = logging.StreamHandler(sys.stdout)
#console.setLevel(logging.DEBUG)
#formatter =  logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
#console.setFormatter(formatter)
#logging.getLogger('name').addHandler(console)
#
##方法1
#logging.basicConfig(level = logging.DEBUG,
#                    format = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
#                    datefmt = '%a, %d %b %Y %H:%M:%S',
#                    filename = 'getHistory.log',
#                    filemode = 'w')
