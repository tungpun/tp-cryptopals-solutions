#!/usr/bin/env python2.7
# This source code is my answer for challenge at http://cryptopals.com/sets/1/challenges/18/

import hashlib
import base64
import re
from Crypto.Cipher import AES
from Crypto import Random
from random import randint

BLOCKSIZE = 16

def xor_rawtext(bigrawtext, rawtext):	
	res = ""
	for i in range(len(rawtext)):
		res += chr(ord(bigrawtext[i]) ^ ord(rawtext[i]))
	return res


def encrypt_oracle(key, plaintext):			
	# In this mode, we dont need use PKCS7 padding
	blocksize = 16			
	aesobj = AES.new(key, AES.MODE_ECB)
	ciphertext = aesobj.encrypt(plaintext)	
	return ciphertext	


def produce_keystream(counter, nonce, key):	

	def int2byte(x):				
		res = ''		
		while x != 0:
			res += chr(x % BLOCKSIZE)
			x = x / BLOCKSIZE		
		return res

	def insert_null_byte(instr, tosize):	
		if len(instr) > tosize:
			raise Exception("len(instr) > tosize")	
		return instr + '\x00' * (tosize - len(instr))

	counterbyte = int2byte(counter)	
	plaintext = insert_null_byte(nonce, BLOCKSIZE/2) + insert_null_byte(counterbyte, BLOCKSIZE/2)	
	return encrypt_oracle(key, plaintext)


def devide_into_blocks(length, thestring):
	blocks = re.findall('.' * length, thestring)		
	blocks.append(thestring[-(len(thestring) % length):])		
	return blocks


THESTRING 	= base64.b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")
NONCE 	 	=  '\x00'			# I am trying to play with binary
KEY 		= "YELLOW SUBMARINE"


if __name__ == "__main__":		
	blocks = devide_into_blocks(BLOCKSIZE, THESTRING)				
	counter = 0
	plaintext = ''
	for block in blocks:		
		keystream = produce_keystream(counter, NONCE, KEY)		
		plaintext += xor_rawtext(keystream, block)
		counter += 1
	print plaintext

