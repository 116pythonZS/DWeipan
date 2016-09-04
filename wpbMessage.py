#!/usr/bin/env python
# -*- coding:cp936 -*-

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
SENDFMT = '!iiiBi7B'
		
class WPBMessage(object):
	def __init__(self, seq, flag, key):
		self.cmdNo = 0
		self.seq = seq
		self.msgSeq = 0
		self.enflag = flag
		self.enkey = key
		
		self.netWorkData = None
		self.__netData = None
		self.__jsonObj = None
	
	def _unpack(self):
		s = struct.Struct(HEADFMT)
		head = s.unpack_from(self.__netData, 0)
		self.cmdNo = head[0]
		self.seq = head[1]
		self.enflag = head[2]
		self.msgSeq = head[3]
		body = self.__netData[s.size:]
		deBody = self.__encrpy(body)
		self.__jsonObj = self.__json(deBody)
	
	def __pack(self, body):
		fmt = SENDFMT + '%dc' % len(body)
		s = struct.Struct(fmt)
		sendDataList = []
		sendDataList.extend([s.size])
		sendDataList.extend([self.cmdNo])
		sendDataList.extend([self.seq])
		sendDataList.extend([self.enflag])
		sendDataList.extend([self.msgSeq])
		sendDataList.extend([0, 0, 0, 0, 0, 0, 0])
		sendDataList.extend(list(body))
		sendData = tuple(sendDataList)
		try:
			self.__netData = s.pack(*sendData)
		except Exception, e:
			print e
			self.__netData = None
	
	def __dict2Str(self, dictData, transfer=1):
		listData = ['{']
		for k in dictData.keys():
			listData.extend('"' + str(k) + '"')
			listData.extend(":")
			if isinstance(dictData[k], (int, long)) and transfer==0:
				listData.extend(str(dictData[k]))
			else:
				listData.extend('"' + str(dictData[k]) + '"')
			listData.extend(",")
		listData[-1] = '}'
		strData = ''.join(listData)
		return strData
	
	def __json(self, data):
		return json.loads(data)
		
	def __encrpy(self, data):
		dedata = None
		try:
			if self.enflag and self.enkey:
				rc4 = RC4(self.enkey)
				dedata = rc4.doEncrpyt(data)
			else:
				dedata = data
		except Exception, e:
			print e, '-[-' + data + '-]-'
			dedata = data
		finally:
			return dedata
			
	def msgFromNetData(self, data):
		self.__netData = data
		self._unpack()
		
	def msgFromJsonObj(self, cmdNo, data, transfer=1):
		self.cmdNo = cmdNo
		self.__jsonObj = data
		body = self.__encrpy(self.__dict2Str(data, transfer))
		self.__pack(body)
	
	def getNetData(self):
		return self.__netData
	
	def getJsonObj(self):
		return self.__jsonObj
		
		