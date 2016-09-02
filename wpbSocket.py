#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    @version: 1.0
    @author : Carrot
    @time   : 16/8/30 19:33
"""

from socket import *
from time import *
import json
import struct
import wpbMessage
import WPBCmd
from Queue import Queue
import threading

PACKAGELEN = 4      # 包长
PACKHEADLEN = 20    # 包头长
BUFSIZE = 1024
HOST = ("wptest.baidao.com", 9103)


class WPBSocket(object):
	def __init__(self, host):
		super.__init__()
		assert host
		self.svr = None
		self.host = host
		self.connect()
	
	def connect(self):
		self.svr = socket(AF_INET, SOCK_STREAM)
		self.svr.recv()
		return self.svr.connect_ex(self.host)
	
	def sendData(self, data):
		self.svr.send(data)

class WThread(threading.Thread):
	def __init__(self, func, args, name = ''):
		threading.Thread.__init__(self)
		self.name = name
		self.func = func
		self.args = args
		self.res = None
	
	def getResult(self):
		return self.res
	
	def run(self):
		self.res = self.func(*self.args)

svr = None
connect_ok = False
sendQ = Queue()

def reader(*args):
	global svr
	while True and connect_ok:
		totalLen = svr.recv(PACKAGELEN)
		length = struct.unpack('!i', totalLen)
		data = svr.recv(length[0] - PACKAGELEN)
		msg = wpbMessage.WPBMessage()
		msg.initFromData(data, '')
		if msg.cmdNo != WPBCmd.AgQuote:
			print msg.getDecrpyResult()
		print msg.getDecrpyResult()
	print 'Reader end'
		
def writer(*args):
	global svr, sendQ
	while True and connect_ok:
		if sendQ and (sendQ.qsize() > 0):
			msg = sendQ.get()
			svr.send(msg.getEncrpyResult())
			if msg.cmdNo != WPBCmd.AgQuote:
				print msg.getEncrpyResult()
			print msg.getEncrpyResult()
	print 'Writer end'

def heartBeat():
	while connect_ok:
		# 添加心跳包
		msg = wpbMessage.WPBMessage()
		msg.cmdNo = WPBCmd.Heartbeat
		msg.encrpyFlag = 0
		
		sleep(60)
			
funcs = (reader, writer, heartBeat)
seq = 0

def testthread():
	global svr, connect_ok
	try:
		svr = socket(AF_INET, SOCK_STREAM)
		svr.connect(HOST)
		connect_ok = True
	except:
		connect_ok = False
		print '出错了'
		
	nfuncs = xrange(len(funcs))
	threads = []
	for i in nfuncs:
		t = WThread(funcs[i], (1,), funcs[i].__name__)
		threads.append(t)
	
	for i in nfuncs:
		threads[i].start()
	
	for i in nfuncs:
		threads[i].join()
		print threads[i].getResult()

def test():
	try:
		global svr
		svr = socket(AF_INET, SOCK_STREAM)
		svr.connect(HOST)
		while True:
			totalLen = svr.recv(PACKAGELEN)
			length = struct.unpack('!i', totalLen)
			data = svr.recv(length[0] - PACKAGELEN)
			msg = wpbMessage.WPBMessage()
			msg.initFromData(data, '')
			if msg.cmdNo != WPBCmd.AgQuote:
				print msg.getResult()
		# print json.dumps(data)
	except Exception, e:
		print e
		
def main():
	try:
		svr = socket(AF_INET, SOCK_STREAM)
		svr.connect(HOST)
		while True:
			lenPack = svr.recv(PACKAGELEN)
			length = struct.unpack('!i', lenPack)
			headLenPack = svr.recv(PACKHEADLEN)
			# length = struct.unpack('!i', lenPack)
			data = svr.recv(length[0] - PACKAGELEN - PACKHEADLEN)
			# print chardet.detect(data)
			print ctime() + '收到数据:Len[%d]' % length
			# print data
			print json.loads(data)
			# print json.dumps(data)
	except Exception, e:
		print e


if __name__ == '__main__':
	testthread()
