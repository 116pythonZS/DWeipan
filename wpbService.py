#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1.0
@author: Carrot 
@contact: huxueli1986@163.com
"""

from socket import *
import struct
from wpbMessage import WPBMessage
import WPBCmd
import threading
from time import *
from Queue import Queue

INT_LEN = 4      # 包长
PACKHEADLEN = 20    # 包头长
BUFSIZE = 1024
HOST = ("wptest.baidao.com", 9103)

HEARTBEAT_INTERVAL = 10
RECONNECT_INTERVAL = 30

class Singleton(type):
    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance = None
    
    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance
    
class WPBService(object):
    __metaclass__ = Singleton
    
    svr = None
    state = 0
    RQueue = Queue()
    WQueue = Queue()
    seq = 0
    encrypt = 0
    enKey = None
    isVistor = 1
    userKey = None
    
    @staticmethod
    def seqId():
        if WPBService.seq < 0:
            WPBService.seq = 0
        WPBService.seq += 1
        return WPBService.seq
    
    @staticmethod
    def reader():
        while True:
            if WPBService.svr and WPBService.state:
                lenPack = WPBService.svr.recv(INT_LEN)
                length = struct.unpack('!i', lenPack)
                data = WPBService.svr.recv(length[0] - INT_LEN)
                msg = WPBMessage(WPBService.enKey)
                msg.initFromNetData(data, WPBService.enKey)
                WPBService.RQueue.put(msg)
            
    @staticmethod
    def dispatchMsg():
        while True:
            if WPBService.RQueue.qsize() and WPBService.state:
                msg = WPBService.RQueue.get()
                print msg.getResult()
            
    
    @staticmethod
    def writer():
        while True:
            if WPBService.svr and WPBService.state:
                # lenPack = WPBService.svr.recv(PACKAGELEN)
                # length = struct.unpack('!i', lenPack)
                # data = WPBService.svr.recv(length[0] - PACKAGELEN)
                # msg = WPBMessage(WPBService.enKey)
                # msg.initFromNetData(data, WPBService.enKey)
                # WPBService.RQueue.put(msg)
                pass
    
    @staticmethod
    def heartbeat():
        while True:
            sleep(HEARTBEAT_INTERVAL)
            if WPBService.svr and WPBService.state:
                msg = WPBMessage(WPBService.enKey)
                data = {"heartbeattime": int(time())}
                msg.initFromLocalData(WPBCmd.Heartbeat, WPBService.enKey,
                                      WPBService.seqId(), WPBService.encrypt, data)
                WPBService.WQueue.put(msg)
    
    @staticmethod
    def reconnect():
        while True:
            pass
            # service = WPBService()
            # service._connect()
            # service._start()
    
    def _connect(self):
        try:
            WPBService.svr = socket(AF_INET, SOCK_STREAM)
            WPBService.svr.connect(HOST)
            WPBService.state = 1
        except Exception, e:
            print e
            WPBService.state = 0
            
    def _start(self):
        threadFunc = [WPBService.reader, WPBService.writer,
                      WPBService.dispatchMsg,
                      WPBService.heartbeat, WPBService.reconnect]
        numList = xrange(len(threadFunc))
        self.threads = []
        for i in numList:
            func = threadFunc[i]
            t = threading.Thread(target = func, name = func.__name__)
            self.threads.append(t)
        
        for i in numList:
            self.threads[i].start()
            
    def run(self):
        self._connect()
        self._start()
        numList = xrange(len(self.threads))
        for i in numList:
            self.threads[i].join()
            
    
    def sendData(self, cmd, data, success=None, fail=None):
        if self.state:
            msg = WPBMessage()
            msg.initFromLocalData(cmd, self.enKey, self.seq, data)
            self.WQueue.put(msg)
        else:
            print '网络连接已经断开,无法发送数据...'


if __name__ == '__main__':
    wpservice = WPBService()
    wpservice.run()
    pass