# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 08:28:35 2018

@author: dell

"""


from watchdog import observers
import time
from observer.FileObserver import DirObserver
from watchdog.utils.bricks import OrderedSetQueue
#    @logevent
#    def on_any_event(self,event):
#        print(" annay ++++++++++++++++++")   

import click

@click.command()
@click.option("--opath",prompt='Enter your observe path:',
              help="your observe path (输入你要检测的路径)",
              default="./file")
@click.option("--recursive",prompt='If recursive (0 == False | 1 == True):',
              help="if events will be emitted for sub-directories traversed recursively (是否检测子目录的文件发生变化)",
              default=0)
def cli(opath,recursive):
    """
        程序主入口使用方法
        python run.py
    """
    observer = observers.Observer(1)
    observer._event_queue = OrderedSetQueue(1)
    event_handler = DirObserver()
    #是否修改循环目录 recursive=false 为不检测path子目录发的任何变化
    observer.schedule(event_handler, opath, recursive=int(recursive))
    observer.start()
    try:
        while True:
            time.sleep(3)
            print("wait")
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("1")
    
def main():
    cli()

if __name__ == '__main__':
    main()
    