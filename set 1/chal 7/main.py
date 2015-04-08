#!/usr/bin/env python2.7
# This source code is my answer for challange at http://cryptopals.com/sets/1/challenges/7/

import hashlib
import base64
from Crypto.Cipher import AES
from Crypto import Random

def main():	
	myAES = AESCipher('YELLOW SUBMARINE')	
	f = open("7.txt", "r")
	ciphertext = f.read().replace('\n', '')	
	f.close()
	plaintext = myAES.decrypt(ciphertext)

def main():	
	f = open("7.txt", "r")	
	ciphertext = f.read().replace('\n', '')	
	f.close()	d
	
	key = 'YELLOW SUBMARINE'

	decobj = AES.new(key, AES.MODE_ECB)
	plaintext = decobj.decrypt(base64.b64decode(ciphertext))
	print plaintext


if __name__ == '__main__':
	main()