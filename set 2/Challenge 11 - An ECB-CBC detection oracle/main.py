#!/usr/bin/env python2.7
# This source code is my answer for challenge at http://cryptopals.com/sets/2/challenges/11/
# too lazy to complete the remainning part of this challenge

import hashlib
import base64
from Crypto.Cipher import AES
from Crypto import Random
from random import randint


def gen_random_key(keylength):
	start = ord('A')
	end = ord('z')	
	key = ""
	for i in range(0, keylength):
		key += chr(randint(start, end+1))
	return key


def encrypt_ECB(plaintext, key):
	aesobj = AES.new(key, AES.MODE_ECB)
	ciphertext = aesobj.encrypt(plaintext)	
	return base64.b64encode(ciphertext)


def decrypt_ECB(ciphertext, key):
	aesobj = AES.new(key, AES.MODE_ECB)
	plaintext = aesobj.decrypt(base64.b64decode(ciphertext))
	return plaintext


def main():		

	iv  = '\x00' * 16
	key = gen_random_key(16)
	print "key:", key

	ciphertext = encrypt_ECB('This is a messag', key)

	print decrypt_ECB(ciphertext, key)



if __name__ == '__main__':
	main()