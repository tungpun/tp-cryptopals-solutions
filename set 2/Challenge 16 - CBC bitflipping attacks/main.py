#!/usr/bin/env python2.7
# This source code is my answer for challenge at http://cryptopals.com/sets/1/challenges/16/
import hashlib
import base64
import re
from Crypto.Cipher import AES
from Crypto import Random
from random import randint


BLOCKSIZE = 16


def make_random_string(keylength):
	start = ord('\x20')
	end = ord('z')	
	key = ""
	for i in range(0, keylength):
		key += chr(randint(start, end+1))
	return key


KEY = make_random_string(16)			# blocksize = 16 is secret
IV = make_random_string(16)			# blocksize = 16 is secret


def PKCS7_padding(text, blocksize):		
	needappend = blocksize - len(text) % blocksize
	return text + chr(needappend) * needappend	


def first_function(instr):	
	instr = re.sub(';', '\x20', instr)
	instr = re.sub('=', '\x20', instr)
	blocksize = 16	
	plaintext = PKCS7_padding("comment1=cooking%20MCs;userdata=" + instr + ";comment2=%20like%20a%20pound%20of%20bacon", blocksize)
	aes = AES.new(KEY, AES.MODE_CBC, IV)
	ciphertext = aes.encrypt(plaintext)
	return ciphertext	


def second_function(ciphertext):
	"""
	This function is protected. 
	Theoretically, you just have read permission and cant change anything
	"""

	blocksize = 16
	aes = AES.new(KEY, AES.MODE_CBC, IV)
	plaintext = aes.decrypt(ciphertext)		
	if ';admin=true;' in plaintext:
		return True
	else:
		return False


def decrypt_oracle(ciphertext):
	"""
	Just a module for me to customize my ciphertext
	"""

	blocksize = 16
	aes = AES.new(KEY, AES.MODE_CBC, IV)
	plaintext = aes.decrypt(ciphertext)		
	return plaintext


def display_xor(s1, s2):
	"""
	For my recognize the change will edit a byte of ciphertext
	"""

	if len(s1) != len(s2):
		raise Exception("Length of two strings is not equal")
	res = ''
	for i in range(len(s1)):
		if s1[i] == s2[i]:
			res += '+'
		else:
			res += '-'
	return res


def is_printable(c):	
	if 32 < ord(c) < 128:
		return True
	return False


def bit_flipping(ciphertext, targetposition, targetvalue):
	"""
	Give my ciphertext, targetposition and targetvalue
	I will return to you the new ciphertext what you need
	"""

	cipherList = list(ciphertext)
	for i in range(256):		
		cipherList[targetposition - BLOCKSIZE] = chr(i)		# Change byte at pos = targetPostion - BLOCKSIZE ...in 256 roung until found '='
		myPlainText = decrypt_oracle(''.join(cipherList))				
		if myPlainText[targetposition] == targetvalue:
			break
	myCipherText = ''.join(cipherList)
	return myCipherText


def display(ciphertext):	
	res = ''
	plaintext = decrypt_oracle(ciphertext)
	for c in plaintext:
		if is_printable(c):
			res += c	
		else:
			res += '_'
	return res


if __name__ == '__main__':	
	origCipherText = first_function(";admin=true;")
	myPlainText = decrypt_oracle(origCipherText)	
	firstPos = myPlainText.find(" admin true ")		
	myCipherText = bit_flipping(origCipherText, firstPos, ';')		
	myCipherText = bit_flipping(myCipherText, firstPos+6, '=')
	myCipherText = bit_flipping(myCipherText, firstPos+11, ';')				
	print "Final result: ", second_function(myCipherText)	
