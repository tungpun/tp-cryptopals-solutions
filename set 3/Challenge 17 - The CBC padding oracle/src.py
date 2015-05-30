#!/usr/bin/env python2.7
# This source code is my answer for challenge at http://cryptopals.com/sets/3/challenges/17/

import base64
import hashlib
from Crypto.Cipher import AES
import random

BLOCKSIZE = 16

def make_random_string(keylength):
	start = ord('\x20')
	end = ord('z')	
	key = ""
	for i in range(0, keylength):
		key += chr(random.randint(start, end+1))
	return key


def PKCS7_padding(text, blocksize):		
	needappend = blocksize - len(text) % blocksize
	return str(text) + chr(needappend) * needappend	


KEY = make_random_string(16)			

def choose_string():	
	f = open("10strings.txt", "r")
	data = f.readlines()
	f.close()
	line = data[random.randint(0, len(data)-1)]
	return base64.b64decode(line)


def first_function():	
	"""
	The first function should select at random one of the following 10 strings
	<10strings.com>
	...generate a random AES key (which it should save for all future encryptions), pad the string out to the 16-byte AES block size and CBC-encrypt it under that key, providing the caller the ciphertext and IV.	
	"""

	plaintext = choose_string()
	iv = make_random_string(16)		
	plaintext = PKCS7_padding(plaintext, BLOCKSIZE)
	aes = AES.new(KEY, AES.MODE_CBC, iv)
	ciphertext = aes.encrypt(plaintext)
	return ciphertext, iv

def bound_zero(i):
	if i < 0:
		i = 0
	return i


def is_valid_pkcs7_padding(plaintext):		
	samplecharacter = plaintext[len(plaintext)-1]	
	if samplecharacter == '\x00':
		return False
	for c in plaintext[bound_zero(len(plaintext)-ord(samplecharacter)):]:
		if c != samplecharacter:
			return False
	return True
	

def second_function(ciphertext, iv):
	"""
	The second function should consume the ciphertext produced by the first function, decrypt it, check its padding, and return true or false depending on whether the padding is valid.
	"""

	blocksize = 16
	aes = AES.new(KEY, AES.MODE_CBC, iv)
	plaintext = aes.decrypt(ciphertext)		
	return is_valid_pkcs7_padding(plaintext)     


def changeCharAt(position, fromString, newCharacter):
	slist = list(fromString)
	slist[position - BLOCKSIZE] = newCharacter
	return ''.join(slist)


def get_padding_byte(ciphertext, iv):	
	lastbytepos = len(ciphertext) - 1

	# Start with position = pos(lastbyte)-1 , loop backwards	
	for itarget in range(lastbytepos-1, bound_zero(lastbytepos-1-BLOCKSIZE), -1):			# loop backwards
		truecnt = 0		
		for i in range(0, 256):
			myciphertext = changeCharAt(itarget, ciphertext, chr(i))							
			if second_function(''.join(myciphertext), iv):			
				truecnt += 1			
		if truecnt == 256:
			return (lastbytepos - itarget)		


if __name__ == '__main__':
	ciphertext, iv = first_function()
	print 'Padding byte: ', get_padding_byte(ciphertext, iv)	
	