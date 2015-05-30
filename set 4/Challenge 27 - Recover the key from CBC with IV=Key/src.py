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
IV = KEY 								# Plz dont :(


def CBC_encrypt(plaintext):		
	"""
	encrypt AES in CBC mode
	"""
	_aes = AES.new(KEY, AES.MODE_CBC, IV)
	_ciphertext = _aes.encrypt(plaintext)
	return _ciphertext	


def CBC_decrypt(ciphertext):
	"""
	decrypt AES in CBC mode
	"""
	
	_aes = AES.new(KEY, AES.MODE_CBC, IV)
	_plaintext = _aes.decrypt(ciphertext)		
	return _plaintext


def bxor(s1, s2):
	if len(s1) != len(s2):
		raise Exception, "In bxor(str, str) function, length of two strings is not equal"
	_r = ''
	for i in range(len(s1)):
		_r += chr(ord(s1[i]) ^ ord(s2[i]))
	return _r

if __name__ == '__main__':	
	secretPlainText = make_random_string(BLOCKSIZE * 3)		
	origCipherText = CBC_encrypt(secretPlainText)
	origCipherTextParts = re.findall('.' * BLOCKSIZE, origCipherText) 
	newCipherText = origCipherTextParts[0] + '\x00' * BLOCKSIZE + origCipherTextParts[0]	 	
	newPlainText = CBC_decrypt(newCipherText)	
	if len(newPlainText) != BLOCKSIZE * 3:
		raise Exception, "Length of newPlainText is not equal (BLOCKSIZE * 3)"
	newPlainTextParts = re.findall('.' * BLOCKSIZE, newPlainText) 

 	print 'random key (encoded hex): ', KEY.encode('hex')
	print 'I found key (encoded hex):', bxor(newPlainTextParts[0], newPlainTextParts[2]).encode('hex')

