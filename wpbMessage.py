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
import ctypes
import json
from wpbRC4 import RC4

HEADFMT = '!iiBI7B'
SENDFMT = '!iiiBI7B'
class WPBMessage(object):
	def __init__(self, key=None):
		self.cmdNo = 0
		self.seq = 0
		self.netWorkData = None
		self.hostData = None
		self.msgSeq = 0
		self.encrpyFlag = 0
		self.key = key
	
	def _unpack(self):
		s = struct.Struct(HEADFMT)
		head = s.unpack_from(self.netWorkData, 0)
		self.cmdNo = head[0]
		self.seq = head[1]
		self.encrpyFlag = head[2]
		self.msgSeq = head[3]
		body = self.netWorkData[s.size:]
		self._decryp(body)
		
	def _pack(self, data):
		self._decryp(data)
		fmt = SENDFMT + '%dB' % len(data)
		s = struct.Struct(fmt)
		buf = ctypes.create_string_buffer(s.size)
		head = [s.size + len(data), self.cmdNo, self.seq, self.encrpyFlag, self.msgSeq]
		s.pack_into(buf, 0, head)
		s.pack_into(buf, s.size, data)
		self.decrpyData = s
		
	def _decryp(self, data):
		try:
			if self.encrpyFlag:
				rc4 = RC4(self.key)
				self.decrpyData = json.load(rc4.doEncrpyt(data))
			else:
				self.decrpyData = json.loads(data)
		except Exception, e:
			print e, '-[-' + data + '-]-'
			
	def initFromNetData(self, data, key):
		self.netWorkData = data
		self.key = key
		self._unpack()
		
	def initFromLocalData(self, cmdNo, key, seq, encrpyFlag, data):
		self.cmdNo = cmdNo
		self.key = key
		self.seq = seq
		self.hostData = data
		self.encrpyFlag = encrpyFlag
		self._pack(data)
		
	def getResult(self):
		return self.decrpyData
		
		