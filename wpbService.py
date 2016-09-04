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
HOST = ("wptest.baidao.com", 9103)
# HOST = ("localhost", 21567)
# HOST = ("localhost", 8888)

HEARTBEAT_INTERVAL = 30
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
        self.svr = None
        self.state = 0
        self.RQueue = Queue()
        self.WQueue = Queue()
        self.seq = 0
        self.enflag = 1
        self.enKey = None
        self.isVistor = 1
        self.userKey = None
        self.reconnect = 0
        self.__threads = None
    
    @staticmethod
    def shared():
        return WPBService()
    # @staticmethod
    def seqId(self):
        if self.seq < 0:
            self.seq = 0
        self.seq += 1
        return self.seq
    
    @staticmethod
    def reader(service):
        while True and service.svr and service.state:
            try:
                lenPack = service.svr.recv(INT_LEN)
                s = struct.Struct('!i')
                length = s.unpack(lenPack)
                data = service.svr.recv(length[0] - INT_LEN)
                msg = WPBMessage(service.seqId(), service.enflag, service.enKey)
                msg.msgFromNetData(data)
                service.RQueue.put(msg)
                print 'Recv cmd[%d] -->'%msg.cmdNo + str(msg.getJsonObj())
                # fmt = '!iiBi7B%dc' % (len(data)-20)
                # s_data = struct.Struct(fmt)
                # tp = s_data.unpack(data)
                # print 'Recv cmd[%d] body-->' % tp[0] + ''.join(tp[11:])
            except socket.error, arg:
                (errno,err_msg) = arg
                print "Connect server failed: %s, errno=%d" % (err_msg,errno)
                service.clear()
            except Exception, e:
                print e
            
    @staticmethod
    def dispatchMsg(service):
        while True:
            if service.RQueue.qsize() and service.state:
                msg = service.RQueue.get()
                data = msg.getJsonObj()
                if msg.cmdNo == WPBCmd.Connect_Socket:
                    service.enflag = data['encryptflag']
                    service.enKey = data['key']
                elif msg.cmdNo == WPBCmd.Heartbeat:
                    pass
                print 'Dispatch cmd[%d] -->'%msg.cmdNo + str(msg.getJsonObj())
                # fmt = '!iiiBi7B%dc' % (len(data)-24)
                # s_data = struct.Struct(fmt)
                # tp = s_data.unpack(data)
                # print 'Dispatch cmd[%d] body-->' % (tp[1]) + ''.join(tp[11:])
    
    @staticmethod
    def writer(service):
        while True:
            if wpservice.WQueue.qsize() and service.state:
                try:
                    msg = service.WQueue.get()
                    data = msg.getNetData()
                    service.svr.send(data)
                    print 'Send cmd[%d] -->' % msg.cmdNo + str(msg.getJsonObj())
                    # fmt = '!iiiBi7B%dc' % (len(data)-24)
                    # s_data = struct.Struct(fmt)
                    # tp = s_data.unpack(data)
                    # # print tp
                    # print 'Send cmd[%d] body-->' % (tp[1]) + ''.join(tp[12:])
                except socket.error, arg:
                    (errno,err_msg) = arg
                    print "Connect server failed: %s, errno=%d" % (err_msg,errno)
                    service.clear()
                except Exception, e:
                    print e
    
    @staticmethod
    def heartbeat(service):
        while service.svr and service.state:
            sleep(HEARTBEAT_INTERVAL)
            msg = WPBMessage(service.seqId(), service.enflag, service.enKey)
            data = {"heartbeattime": int(time())}
            msg.msgFromJsonObj(WPBCmd.Heartbeat, data)
            service.WQueue.put(msg)
    
    @staticmethod
    def reconnectThread(service):
        
        while not (service.svr and service.state and service.reconnect):
            service.reconnect = 1
            service.__connect()
            service.reconnect = 0
            if service.svr and service.state:
                service.run()
            sleep(10)

    
    def reconnect(self):
        while not (self.svr and self.state):
            func = WPBService.reconnect
            t = threading.Thread(target=func, name=threading.__name__, args=(self,))
            t.start()
            t.join()
            sleep(5)

    # @staticmethod
    def clear(self):
        self.svr = None
        self.state = 0
        self.RQueue = Queue()
        self.WQueue = Queue()
        self.seq = 0
        self.enflag = 0
        self.enKey = None
        self.isVistor = 1
        self.userKey = None
        self.reconnect = 0
        
    def __connect(self):
        try:
            self.svr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.svr.connect(HOST)
            self.state = 1
            msg = WPBMessage(self.seqId(), self.enflag, self.enKey)
            msg.msgFromJsonObj(cmdNo=WPBCmd.Connect_Socket, data=CONNECT_BODY, transfer=0)
            self.WQueue.put(msg)
        except socket.error, arg:
            (errno, err_msg) = arg
            print "Connect server failed: %s, errno=%d" % (err_msg, errno)
            self.clear()
        except Exception, e:
            print e
            
    def __start(self):
        # threadFunc = [WPBService.reader, WPBService.writer,
        #               WPBService.dispatchMsg,
        #               WPBService.heartbeat, WPBService.reconnect]
        threadFunc = [WPBService.reader, WPBService.writer,
                      WPBService.dispatchMsg, WPBService.heartbeat]
        numList = xrange(len(threadFunc))
        self.__threads = []
        for i in numList:
            func = threadFunc[i]
            t = threading.Thread(target=func, name=func.__name__, args=(self,))
            self.__threads.append(t)
        
        for i in numList:
            self.__threads[i].start()
            
    def run(self):
        self.__connect()
        self.__start()
        numList = xrange(len(self.__threads))
        for i in numList:
            self.__threads[i].join()
            
    
    def sendData(self, cmd, data, success=None, fail=None):
        if self.state:
            msg = WPBMessage(self.seqId(), self.enflag, self.enKey)
            msg.msgFromJsonObj(cmd, data)
            self.WQueue.put(msg)
        else:
            print '网络连接已经断开,无法发送数据...'


if __name__ == '__main__':
    wpservice = WPBService()
    wpservice.run()
    {}.keys()
    pass