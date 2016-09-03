#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1.0
@author: Carrot 
@contact: huxueli1986@163.com
"""

import socket
import sys
import struct
from wpbMessage import WPBMessage
import WPBCmd
import threading
from time import *
from Queue import Queue

INT_LEN = 4      # 包长
PACKHEADLEN = 20    # 包头长
BUFSIZE = 1024
# HOST = ("wptest.baidao.com", 9103)
# HOST = ("localhost", 21567)
HOST = ("localhost", 8888)

HEARTBEAT_INTERVAL = 10
RECONNECT_INTERVAL = 30

CONNECT_BODY = {
    "md5key": "f48d6984f654327d9e83b2668e9b6f54",
    "deviceId": "A9206F54-B8C5-4D01-9252-C502C09FF35C",
    "os": "iPhone OS 9.3",
    "encryptflag": 1,
    "clientversion": "1.0",
    "clienttype": 10005,
    "visitor": 0,
    "keystring": "13816254394"
}

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

    def __init__(self, *args, **kw):
        super(WPBService, self).__init__(*args, **kw)
    
    @staticmethod
    def shared():
        return WPBService()
    @staticmethod
    def seqId():
        if WPBService.seq < 0:
            WPBService.seq = 0
        WPBService.seq += 1
        return WPBService.seq
    
    @staticmethod
    def reader():
        while True and WPBService.svr and WPBService.state:
            try:
                lenPack = WPBService.svr.recv(INT_LEN)
                s = struct.Struct('!i')
                length = s.unpack(lenPack)
                data = WPBService.svr.recv(length[0] - INT_LEN)
                msg = WPBMessage(WPBService.enKey)
                msg.initFromNetData(data, WPBService.enKey)
                WPBService.RQueue.put(msg)
                fmt = '!iiBi7B%dc' % (len(data)-20)
                s_data = struct.Struct(fmt)
                tp = s_data.unpack(data)
                print 'Recv cmd[%d] body-->' % tp[0] + ''.join(tp[11:])
            except socket.error, arg:
                (errno,err_msg) = arg
                print "Connect server failed: %s, errno=%d" % (err_msg,errno)
                WPBService.clear()
            except Exception, e:
                print e
            
    @staticmethod
    def dispatchMsg():
        while True and WPBService.RQueue.qsize() and WPBService.state:
            msg = WPBService.RQueue.get()
    
    @staticmethod
    def writer():
        while True and WPBService.WQueue.qsize() and WPBService.state:
            try:
                msg = WPBService.WQueue.get()
                WPBService.svr.send(msg.getResult())
                data = msg.getResult()
                fmt = '!iiiBi7B%dc' % (len(data)-24)
                s_data = struct.Struct(fmt)
                tp = s_data.unpack(data)
                # print tp
                print 'Send cmd[%d] body-->' % (tp[1]) + ''.join(tp[12:])
            except socket.error, arg:
                (errno,err_msg) = arg
                print "Connect server failed: %s, errno=%d" % (err_msg,errno)
                WPBService.clear()
            except Exception, e:
                print e
    
    @staticmethod
    def heartbeat():
        while WPBService.svr and WPBService.state:
            sleep(HEARTBEAT_INTERVAL)
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
    
    @staticmethod
    def clear():
        WPBService.svr = None
        WPBService.state = 0
        WPBService.RQueue = Queue()
        WPBService.WQueue = Queue()
        WPBService.seq = 0
        WPBService.encrypt = 0
        WPBService.enKey = None
        
    def _connect(self):
        try:
            WPBService.svr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            WPBService.svr.connect(HOST)
            WPBService.state = 1
            msg = WPBMessage()
            msg.initFromLocalData(cmdNo=WPBCmd.Connect_Socket, key=None,
                                  encrpyFlag=0, seq=self.seqId(),
                                  data=CONNECT_BODY, transfer=0)
            WPBService.WQueue.put(msg)
        except socket.error, arg:
            (errno, err_msg) = arg
            print "Connect server failed: %s, errno=%d" % (err_msg, errno)
            WPBService.clear()
        except Exception, e:
            print e
            
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