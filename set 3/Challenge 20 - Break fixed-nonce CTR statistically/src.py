#!/usr/bin/env python2.7
# This source code is my answer for challenge at http://cryptopals.com/sets/1/challenges/20
# TODO, not completed

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
		for i in range(len(rawtext)):
			res += chr(ord(bigrawtext[i]) ^ ord(rawtext[i]))
		return res


	blocks = devide_into_blocks(BLOCKSIZE, thestring)				
	counter = 0
	output = ''
	for block in blocks:		
		keystream = produce_keystream(counter, NONCE, KEY)				
		output += xor_rawtext(keystream, block)
		counter += 1
	return output


def first_encrypt():
	f = open('20.txt', 'r')
	lines = f.readlines()	
	f.close()
	ciphertexts = []
	for line in lines:
		ciphertexts.append(crypt_ctr(base64.b64decode(line), KEY))		
	return ciphertexts


def mxor_rawtext(rawtext1, rawtext2):	
	if len(rawtext1) < len(rawtext2):
		rawtext1, rawtext2 = rawtext2, rawtext1
	# now, len(rawtext1) >= len(rawtext2)
	rawtext2 += '\x00' * (len(rawtext1) - len(rawtext2))
	res = ""			
	for i in range(len(rawtext1)):
		res += chr(ord(rawtext1[i]) ^ ord(rawtext2[i]))
	return res


def break_ctr(ciphertexts):
	def get_pair_with_an_entry(eid, ciphertexts):
		firstentry = ciphertexts[eid]
		pairs = []
		for i in range(0, len(ciphertexts)):
			pairs.append(mxor_rawtext(firstentry, ciphertexts[i]))
		return pairs

	def guest_characters_of_an_entry(pairs, keyword):
		#total = []
		#for i in range(100):
		#	total.append('+')

		def do_clean(s):
			res = ''
			for i in range(len(s)):
				c = s[i]
				if '\x20' <= c <= 'z':
					res += c
				else:
					res += '_'
					#total[i] = '_'
			return res		
		cnt = 0
		for pair in pairs:
			print '%02d' % cnt, do_clean(mxor_rawtext(pair, keyword))
			cnt += 1
		#print '   ' + ''.join(total)


	
	keyword = 'Program' + '\x00' * 30
	seid = 29

	for eid in range(seid, seid + 1):
		print "eid: ", eid		

		pairs0 = get_pair_with_an_entry(eid, ciphertexts)	
		guest_characters_of_an_entry(pairs0, keyword)
		print "\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n\n"


if __name__ == '__main__':	
	ciphertexts = first_encrypt()
	break_ctr(ciphertexts)
