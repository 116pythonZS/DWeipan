#!/usr/bin/env python
# -*- coding:cp936 -*-

"""
    @version: 1.0
    @author : Carrot
    @time   : 16/8/30 20:52
"""

# typedef struct
# {
#     int wCmd; //�����
#     int wSeq; //�������к�,ҵ��ʹ��,ת�����ٹ���
#     unsigned char  bEncryptFlag; //���ܱ�־(0: �� ����1:���� )
#     int wKeySeq;
#     unsigned char  sReserved[7];
# } WeixinPkgHead; //Э���ͷ
# typedef struct
# {
#     WeixinPkgHead stWeixinPkgHead;
#     unsigned char   sBody[0];
# } WeixinPkg; //Э���
#
# ���ݰ�����(4+20+���峤��) + ��ͷ + ����

import struct
import ctypes
import json
from wpbRC4 import RC4

HEADFMT = '!iiBI7B'
SENDFMT = '!iiiBi7B'
class WPBMessage(object):
	def __init__(self, key=None):
		self.cmdNo = 0
		self.seq = 0
		self.netWorkData = None
		self.hostData = None
		self.msgSeq = 0
		self.encrpyFlag = 0
		self.key = key
		self.decrpyData = None
	
	def _unpack(self):
		s = struct.Struct(HEADFMT)
		head = s.unpack_from(self.netWorkData, 0)
		self.cmdNo = head[0]
		self.seq = head[1]
		self.encrpyFlag = head[2]
		self.msgSeq = head[3]
		body = self.netWorkData[s.size:]
		self._decryp(body)
		self._json(self.decrpyData)
	
	def _pack(self, data):
		fmt = SENDFMT + '%dc' % len(self.decrpyData)
		s = struct.Struct(fmt)
		buf = ctypes.create_string_buffer(s.size)
		sendDataList = []
		sendDataList.extend([s.size + len(self.decrpyData)])
		sendDataList.extend([self.cmdNo])
		sendDataList.extend([self.seq])
		sendDataList.extend([self.encrpyFlag])
		sendDataList.extend([self.msgSeq])
		sendDataList.extend([0, 0, 0, 0, 0, 0, 0])
		sendDataList.extend(list(self.decrpyData))
		sendData = tuple(sendDataList)
		try:
			self.decrpyData = s.pack(*sendData)
			pass
		except Exception, e:
			print e
		
	# def _pack(self, data):
	# 	self._decryp(self._dict2Str(data))
	# 	print len(self.decrpyData)
	# 	fmt = SENDFMT + '%dB' % len(self.decrpyData)
	# 	s = struct.Struct(fmt)
	# 	buf = ctypes.create_string_buffer(s.size)
	# 	head = (s.size + len(data), self.cmdNo, self.seq, self.encrpyFlag, self.msgSeq, ord(chr(0)),
	# 	ord(chr(0)), ord(chr(0)), ord(chr(0)), ord(chr(0)), ord(chr(0)), ord(chr(0)), self.decrpyData)
	# 	# s.pack_into(buf, 0, *head)
	# 	# s.pack_into(buf, s.size, data)
	# 	try:
	# 		s.pack(fmt, *head)
	# 	except Exception, e:
	# 		print e
	# 	self.decrpyData = s
	
	def _dict2Str(self, dictData, transfer=1):
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
	
	def _json(self, data):
		return json.load(data)
		
	def _decryp(self, data):
		try:
			if self.encrpyFlag and self.key:
				rc4 = RC4(self.key)
				self.decrpyData = rc4.doEncrpyt(data)
			else:
				self.decrpyData = data
		except Exception, e:
			print e, '-[-' + data + '-]-'
			
	def initFromNetData(self, data, key):
		self.netWorkData = data
		self.key = key
		self._unpack()
		
	def initFromLocalData(self, cmdNo, key, seq, encrpyFlag, data, transfer=1):
		self.cmdNo = cmdNo
		self.key = key
		self.seq = seq
		self.hostData = data
		self.encrpyFlag = encrpyFlag
		self._decryp(self._dict2Str(data, transfer))
		self._pack(data)
		
	def getResult(self):
		return self.decrpyData
		
		