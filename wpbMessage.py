#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    @version: 1.0
    @author : Carrot
    @time   : 16/8/30 20:52
"""

# typedef struct
# {
#     int wCmd; //命令号
#     int wSeq; //包的序列号,业务使用,转发不再关心
#     unsigned char  bEncryptFlag; //加密标志(0: 不 加密1:加密 )
#     int wKeySeq;
#     unsigned char  sReserved[7];
# } WeixinPkgHead; //协议包头
# typedef struct
# {
#     WeixinPkgHead stWeixinPkgHead;
#     unsigned char   sBody[0];
# } WeixinPkg; //协议包
#
# 数据包长度(4+20+包体长度) + 包头 + 包体

import struct
import json
from wpbRC4 import RC4

HEADFMT = '!iiBI7B'
class WPBMessage(object):
	def __init__(self, key=None):
		self.encrpyData = None
		self.msgSeq = 0
		self.key = key
		# self._unpack()
	
	def _unpack(self):
		s = struct.Struct(HEADFMT)
		head = s.unpack_from(self.encrpyData, 0)
		self.cmdNo = head[0]
		self.seq = head[1]
		self.encrpyFlag = head[2]
		self.msgSeq = head[3]
		self._decryp()
		
	def _decryp(self):
		s = struct.Struct(HEADFMT)
		body = self.encrpyData[s.size:]
		if self.encrpyFlag:
			rc4 = RC4(self.key)
			self.decrpyData = json.load(rc4.doEncrpyt(body))
		else:
			self.decrpyData = json.loads(body)
			
	def initFromData(self, data, key):
		self.encrpyData = data
		self.key = key
		self._unpack()
		
	def getResult(self):
		return self.decrpyData
		
		