#!/usr/bin/env python2.7
# This source code is my answer for challange at http://cryptopals.com/sets/1/challenges/10/

import hashlib
import base64
from Crypto.Cipher import AES
from Crypto import Random

def main():	
	f = open("10.txt", "r")	
	ciphertext = f.read().replace('\n', '')	
	f.close()	

	iv  = '\x00' * 16
	key = 'YELLOW SUBMARINE'

	decobj = AES.new(key, AES.MODE_CBC, iv)
	plaintext = decobj.decrypt(base64.b64decode(ciphertext))
	print plaintext


if __name__ == '__main__':
	main()