#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1.0
@author: Carrot 
@contact: huxueli1986@163.com
@software: PyCharm
@file: singleton.py
@time: 16-9-1 下午10:59
"""

# 方法一
class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None
    
    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton,cls).__call__(*args, **kw)
        return cls.instance

class MyClass1(object):
    __metaclass__ = Singleton

# 方法二
def singleton2(cls,*args,**kw):
    instances = {}
    
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args,**kw)
        return instances[cls]
    
    return _singleton

@singleton2
class MyClass2(object):
    a = 1
    
    def __init__(self,x=0):
        self.x = x


# 方法三
class Singleton3(type):
    def __init__(cls,name,bases,dict):
        super(Singleton2,cls).__init__(name,bases,dict)
        cls._instance = None
    
    def __call__(cls,*args,**kw):
        if cls._instance is None:
            cls._instance = super(Singleton2,cls).__call__(*args,**kw)
        return cls._instance


class MyClass3(object):
    __metaclass__ = Singleton2
    
# 方法四
class Borg(object):
    _state = {}
    
    def __new__(cls,*args,**kw):
        ob = super(Borg,cls).__new__(cls,*args,**kw)
        ob.__dict__ = cls._state
        return ob

class MyClass4(Borg):
    a = 1

if __name__ == '__main__':
    pass