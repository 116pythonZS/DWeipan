#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1.0
@author: Carrot 
@contact: huxueli1986@163.com
"""

# from __future__ import print_function
from twisted.internet import reactor
from twisted.internet import protocol

import struct
import wpbMessage
import WPBCmd


# HOST = ("wptest.baidao.com", 9103)
HOST = ("localhost", 8000)

class WPBSvrProtocol(protocol.Protocol):
    def __init__(self):
        # protocol.Protocol.__init__(self)
        pass
    def connectionMade(self):
        pass
    
    def connectionLost(self, reason):
        print reason
        pass
    
    def dataReceived(self, data):
        print data
        pass
    
class WPBSvrFactory(protocol.ReconnectingClientFactory):
    protocol = WPBSvrProtocol
    def __init__(self):
        # protocol.ReconnectingClientFactory.__init__(self)
        pass
    
    def clientConnectionLost(self, connector, reason):
        print reason
        pass
    
    def clientConnectionFailed(self, connector, reason):
        print reason
        pass
    pass


class Singleton(type):
    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance = None
    
    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class WPBService(object, protocol.ReconnectingClientFactory):
    __metaclass__ = Singleton
    # protocol = WPBService
    #
    # def __init__(self):
    #     super(ReconnectingClientFactory, self).__init__(self)
    #
    # def clientConnectionLost(self, connector, reason):
    #     pass
    #
    # def clientConnectionFailed(self, connector, reason):
    #     pass
    #
    # def sendDataWithCallBack(self, cmd, data, success, fail):
    #     pass
    
    def connect(self):
        f = WPBSvrFactory()
        reactor.connectTCP('localhost', 8000, f)
        reactor.run()
        
    def sendData(self, cmd, data, callback):
        print data
        pass


if __name__ == '__main__':
    wpb = WPBService()
    wpb.connect()
    wpb.sendData(3002, 'ssssss', None);