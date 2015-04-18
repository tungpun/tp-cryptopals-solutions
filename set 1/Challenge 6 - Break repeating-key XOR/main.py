#!/usr/bin/env python2.7
# This source code is my answer for challenge at http://cryptopals.com/sets/1/challenges/6/
# I still have many things to do before finishing it

import binascii
import sys
import base64
import re
from random import randint

MAXINT = 10000

def strHamming(s1, s2):
	difCnt = 0
	for i in range(0, len(s1)):
		if s1[i] != s2[i]:
			difCnt += 1
	return difCnt


def bin8(c):
	return bin(ord(c))[2:].zfill(8)


def binHamming(s1, s2):
	n = len(s1)
	s1bin = ""
	for c in s1:
		s1bin += bin8(c)
	
	s2bin = ""
	for c in s2:
		s2bin += bin8(c)

	difCnt = 0
	for i in range(0, len(s1bin)):		
		if s1bin[i] != s2bin[i]:
			difCnt += 1
	return difCnt


def min2(a, b):
	if a < b:
		return a
	return b


def find_key_size(data):	
	print "=================== FIND KEY SIZE ==================="	
	n = len(data)
	minkeysize = MAXINT
	minkey = -1
	for keysize in range(2, min2(n/2, 35)):		
		
		p = []
		for i in range(1, n/keysize+1):						
			p.append(data[keysize*(i-1):keysize*i])			

		sumHammingDistance = 0		
		cntrepeated = 10000		
		for i in range(0, 10000):			
			first = p[randint(0, len(p)-1)]
			second = p[randint(0, len(p)-1)]			
			sumHammingDistance += float(binHamming(first, second) / keysize)								

		print keysize, sumHammingDistance / cntrepeated

		if sumHammingDistance / cntrepeated < minkeysize:
			minkeysize = sumHammingDistance / cntrepeated
			minkey = keysize
	return minkey


def is_prinable(r):
	return (r == 10) or (32 <= r < 128)	


def find_key(keysize, data):
	print "=================== FIND KEY ==================="	
	blocks = re.findall('.'*keysize*2, data)	
	
	key = ''

	for ikey in range(0, keysize):		# Find key character at position ikey
		print "Key[" + str(ikey) + "] = ",
		for i in range(10, 128):		# Try all posible of key char, which is prinable. You can expand it
			keychar = chr(i)		
			ok = 0	

			for block in blocks:			
				block = block.decode('hex')				
				r = ord(block[ikey]) ^ ord(keychar)				
				if is_prinable(r):			
					ok += 1						
			if len(blocks) - ok == 0:						
				print '[' + keychar + ']', 
				
		print ''


def main():
	f = open("6.txt", "r")
	data = f.read()
	f.close()
	data = base64.b64decode(data).encode('hex') 				
	
	keySize = find_key_size(data)
	keysize = 29
	print "Keysize = " + str(keysize)	
	

	find_key(keysize, data)
					

if __name__ == '__main__':
	main()