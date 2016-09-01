#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1.0
@author: Carrot 
@contact: huxueli1986@163.com
"""

from socket import *
import struct
import wpbMessage
import WPBCmd


class Singleton(type):
    def __init__(cls,name,bases,dict):
        super(Singleton,cls).__init__(name,bases,dict)
        cls.instance = None
    
    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton,cls).__call__(*args, **kw)
        return cls.instance
    
class WPBService(object):
    __metaclass__ = Singleton
    
    def _connect(self):
        self.svr = socket(AF_INET, SOCK_STREAM)
        self.svr.connect(HOST)

    def sendDataWithCallBack(self, cmd, data, callback):
        pass
    
    def sendData(self, cmd, data, callback):
        pass


if __name__ == '__main__':
    pass