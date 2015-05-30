#!/usr/bin/env python2.7
# This source code is my answer for challenge at http://cryptopals.com/sets/4/challenges/25/

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


NONCE 	 	=  '\x00'			# I am trying to play with binary
KEY 		= make_random_string(16)


def crypt_ctr(thestring):

	def devide_into_blocks(length, thestring):		
		blocks = re.findall('.' * length, thestring)		
		if len(thestring) % length == 0:
			return blocks			# coz thestring[-0:] = thestring
		blocks.append(thestring[-(len(thestring) % length):])		
		return blocks

	def produce_keystream(counter, nonce, KEY):	
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
		def encrypt_oracle(KEY, plaintext):			
			# In this mode, we dont need use PKCS7 padding
			blocksize = 16			
			aesobj = AES.new(KEY, AES.MODE_ECB)
			ciphertext = aesobj.encrypt(plaintext)	
			return ciphertext	
		counterbyte = int2byte(counter)	
		plaintext = insert_null_byte(nonce, BLOCKSIZE/2) + insert_null_byte(counterbyte, BLOCKSIZE/2)	
		return encrypt_oracle(KEY, plaintext)

	def xor_rawtext(bigrawtext, rawtext):	
		res = ""		
		for i in range(len(rawtext)):
			res += chr(ord(bigrawtext[i]) ^ ord(rawtext[i]))
		return res


	blocks = devide_into_blocks(BLOCKSIZE, thestring)				
	counter = 0
	output = ''
	for block in blocks:		
		KEYstream = produce_keystream(counter, NONCE, KEY)				
		output += xor_rawtext(KEYstream, block)
		counter += 1
	return output




def encrypt_given_text():
	f = open('20.txt', 'r')	
	_givenText = base64.b64decode(f.read())			
	f.close()

	return crypt_ctr(_givenText)


def edit(ciphertext, offset, newtext):
	newcipher = crypt_ctr(newtext)
	return ciphertext[:offset] + newcipher


if __name__ == "__main__":			
	cipherText = encrypt_given_text()
	# Normal case:	
	print 'Normal case:', edit(cipherText, 10, 'sample-newtext')
	# But...
	print 'But...', edit(cipherText, 0, cipherText)
