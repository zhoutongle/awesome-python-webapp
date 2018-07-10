#!/usr/bin/python
#coding=utf-8
import sys
import os
import re
import datetime
import dircache
from Queue import Queue
import subprocess
import threading
import traceback
import time
#import fcntl
from time import ctime,sleep
from read_utils import say_word
from cpu_utils import *

currpath = os.path.join(os.getcwd(), os.path.dirname(__file__))
if not currpath in sys.path:
    sys.path.append(currpath)

utilspath = os.path.join(currpath, 'utils')
if not utilspath in sys.path:
    sys.path.append(utilspath)

WARN_INFO_PATH = "\\".join(currpath.split("\\")[:-2]) + "\\data\\warn_info.txt"

def start_process():
    warn_info = []
    monitor_info_queue = Queue(1000)
    threads = []
    try:
        t1 = threading.Thread(name="get_cpu_mem", target=get_cpu_mem_info, args=(monitor_info_queue, ))
        threads.append(t1)
        
        for th in threads:
            th.setDaemon(True)
            th.start()
    except:
        print traceback.format_exc()
     
    while True:
        try:
            monitor_info = monitor_info_queue.get()
            if monitor_info:
                with open(WARN_INFO_PATH, "r") as f:
                    file_content = f.read()
                    if file_content:
                        warn_info = eval(file_content)
                    warn_info.append(monitor_info)
                with open(WARN_INFO_PATH, "w") as f:
                    f.write("%s" % warn_info)
                say_word(monitor_info['message'])
        except:
            print traceback.format_exc()
    
    for th in threads:
        th.join()
        
#if __name__ == '__main__':
    #start_process()