#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    @version: 1.0
    @author : Carrot
    @time   : 16/8/31 11:09
"""

class RC4:
	def __init__(self, key = None, boxLen = 256):
		assert boxLen > 0
		self.key = key
		self.keylen = len(key)
		self.boxLen = boxLen
		self._box()
	
	def _box(self):
		self.box = range(self.boxLen)
		x = 0
		for i in range(256):
			x = (x + self.box[i] + ord(self.key[i % len(self.key)])) % self.boxLen
			self.box[i], self.box[x] = self.box[x], self.box[i]
		print "box = ", self.box
			
	def _process(self, srcData):
		x = 0
		y = 0
		outData = []
		for index in srcData:
			x = (x + 1) % self.boxLen
			# numx = self.box[x]
			y = (y + self.box[x]) % self.boxLen
			# numy = self.box[y]
			self.box[x], self.box[y] = self.box[y], self.box[y]
			# indexK = self.box[(numx + numy) % self.boxLen]
			outData.append(chr(ord(index) ^ self.box[(self.box[x] + self.box[y]) % self.boxLen]))
		return ''.join(outData)
		
	
	def encode(self, string):
		return self._process(string)
	
	def decode(self, string):
		return self._process(string)
	

def rc4crpty(data, key):
	x = 0
	box = range(256)
	for i in range(256):
		x = (x + box[i] + ord(key[i % len(key)])) % 256
		box[i], box[x] = box[x], box[i]
	x = 0
	y = 0
	out = []
	for char in data:
		x = (x + 1) % 256
		y = (y + box[x]) % 256
		box[x], box[y] = box[y], box[x]
		out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
	
	return ''.join(out)

if __name__ == '__main__':
	rc4 = RC4('a', 256)
	# data = '{"code":"200","seq":"28525482373873664","result":"4.065","lasttime":"1472621553","lastprice":"4.064"}'
	data = 'h'
	print 'src --> ', data
	enData = rc4.encode(data)
	print 'encrpty --> ', enData
	deData = rc4.decode(enData)
	print 'decrpty --> ', deData
	