#!/usr/bin/env python2.7
# This source code is my answer for challenge at http://cryptopals.com/sets/1/challenges/19/

import hashlib
import base64
import re
from Crypto.Cipher import AES
from Crypto import Random
from random import randint


def make_random_string(keylength):
	return 'A' * keylength
	start = ord('\x20')
	end = ord('z')	
	key = ""
	for i in range(0, keylength):
		key += chr(randint(start, end+1))
	return key


BLOCKSIZE = 16
NONCE =  '\x00'			# I am trying to play with binary
KEY = make_random_string(BLOCKSIZE)

def crypt_ctr(thestring, key):

	def devide_into_blocks(length, thestring):		
		blocks = re.findall('.' * length, thestring)		
		if len(thestring) % length == 0:
			return blocks			# coz thestring[-0:] = thestring
		blocks.append(thestring[-(len(thestring) % length):])		
		return blocks

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
		def encrypt_oracle(key, plaintext):			
			# In this mode, we dont need use PKCS7 padding
			blocksize = 16			
			aesobj = AES.new(key, AES.MODE_ECB)
			ciphertext = aesobj.encrypt(plaintext)	
			return ciphertext	
		counterbyte = int2byte(counter)	
		plaintext = insert_null_byte(nonce, BLOCKSIZE/2) + insert_null_byte(counterbyte, BLOCKSIZE/2)	
		return encrypt_oracle(key, plaintext)

	def xor_rawtext(bigrawtext, rawtext):	
		res = ""
		print '[DEBUG]', len(bigrawtext), len(rawtext)
		for i in range(len(rawtext)):
			res += chr(ord(bigrawtext[i]) ^ ord(rawtext[i]))
		return res


	blocks = devide_into_blocks(BLOCKSIZE, thestring)				
	counter = 0
	output = ''
	for block in blocks:		
		keystream = produce_keystream(counter, NONCE, KEY)		
		print keystream.encode('hex')
		output += xor_rawtext(keystream, block)
		counter += 1
	return output


def first_encrypt():
	f = open('data', 'r')
	lines = f.readlines()
	f.close()
	ciphertexts = []
	for line in lines:
		ciphertexts.append(crypt_ctr(base64.b64decode(line), KEY))
	return ciphertexts


if __name__ == '__main__':	
	ciphertexts = first_encrypt()
