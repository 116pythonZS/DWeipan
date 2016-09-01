#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@version: 1.0
@author : Carrot
@time   : 16/9/1 20:30

该类定义了一个方法__setattr()__，和一个异常ConstError, ConstError类继承
自类TypeError. 通过调用类自带的字典__dict__, 判断定义的常量是否包含在字典中。
如果字典中包含此变量，将抛出异常，否则，给新创建的常量赋值。
最后把const类注册到sys.modules这个全局字典中。
"""


import sys

class _const(object):
	class ConstError(TypeError):
		pass
	
	def __setattr__(self, key, value):
		if key in self.__dict__:
			raise self.ConstError, "不能重新定义常量(%s)" % key
		self.__dict__[key] = value
		
sys.modules[__name__] = _const()
