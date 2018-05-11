# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 08:28:35 2018

@author: dell
"""


from watchdog import observers
#from watchdog.events import FileModifiedEvent,DirModifiedEvent,FileSystemEventHandler,LoggingEventHandler
from watchdog.events import FileSystemEventHandler,FileModifiedEvent
import time
from utils.logUtil import util

from rabbitmq.producer import Producer,postPanelData
import logging

logger = logging.getLogger("mylogger")

class DirObserver(FileSystemEventHandler):
    """
        文件目录监控器，同时监控器内置了消费队列连接对象，传输修改的文件
        这里修改的文件需要做经一部处理(event))
            print("except file modify")
    @util.logger一个Producer对象，用以保证在修改文件的时候做操作
        """
    def __init__(self):
        FileSystemEventHandler.__init__(self)
        self.producer = Producer()
        logger.info("DirObserver+++++++++++++++++")
    @util.logger
    def on_modified(self,event):
        print("是否是文件夹%d"%event.is_directory)
        if isinstance(event,FileModifiedEvent): 
            logger.info("file is modifed!")
            if isinstance(self.producer,Producer):   
                #这里处理文件 tsne等操作
                self.producer.pushData(postPanelData())
            else:
                logger.info("不是 producer")
        else:
            print(type(event))
            print("except file modify")
    @util.logger
    def on_moved(self,event):
        print(" move ++++++++++++++++++")
    @util.logger    
    def on_created(self,event):
        print(" create ++++++++++++++++++")
    @util.logger
    def on_deleted(self,event):
        print(" delete ++++++++++++++++++")
#    @logevent
#    def on_any_event(self,event):
#        print(" annay ++++++++++++++++++")   


if __name__ == '__main__':
    path = r"E:\zhangll\20170623子空间谱聚类分析\FSC\FscDemo\code\t-sne-tensorflow\file"
    observer = observers.Observer(1)
    event_handler = DirObserver()
    #是否修改循环目录 recursive=false 为不检测path子目录发的任何变化
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(3)
            #print("wait")
    except KeyboardInterrupt:
        observer.stop()
#    observer.join()
    print("1")

