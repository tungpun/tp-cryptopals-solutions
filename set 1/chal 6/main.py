#/usr/bin python2.7
# This source code is my answer for challange at http://cryptopals.com/sets/1/challenges/6/
# I still have many things to do before finishing it

import binascii
import sys
import base64
import re
from random import randint


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




def main():
	f = open("7.txt", "r")
	data = f.read()
	f.close()
	data = base64.b64decode(data) 				
	print len(data)
	# find_key_size(data)
	keysize = 3
	blocks = re.findall('.'*keysize, data)

	for i in range(1, 256):
		keychar = chr(i)		
		ok = 0	
		for block in blocks:			
			r = ord(block[0]) ^ ord(keychar)
			if 32 <= r <= 160:				
				ok += 1				
		if len(blocks) - ok == 0:		
			print keychar, i, len(blocks) - ok



if __name__ == '__main__':
	main()