#!/usr/bin/env python2.7
# This source code is my answer for challenge at http://cryptopals.com/sets/2/challenges/14/

import hashlib
import base64
import re
from Crypto.Cipher import AES
from Crypto import Random
from random import randint


UNKNOWN_STRING = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"


def make_random_string(keylength):
	start = ord('\x20')
	end = ord('z')	
	key = ""
	for i in range(0, keylength):
		key += chr(randint(start, end+1))
	return key


def make_random_prefix():
	rplen = randint(4, 128)	
	return make_random_string(rplen)	


KEY = make_random_string(16)			# blocksize = 16 is secret
RANDOM_PREFIX = make_random_prefix()


def encrypt_oracle(plaintext):		
	"""
	In realistic challenges, everything in this function is secret..... ignore it :D
	"""		
	blocksize = 16		
	plaintext = PKCS7_padding(RANDOM_PREFIX + plaintext + base64.b64decode(UNKNOWN_STRING), blocksize)	
	aesobj = AES.new(KEY, AES.MODE_ECB)
	ciphertext = aesobj.encrypt(plaintext)	
	return ciphertext	


def PKCS7_padding(text, blocksize):		
	needappend = blocksize - len(text) % blocksize
	return text + chr(needappend) * needappend	


def get_block_size(encrypt_oracle):		
	"""
	try until have different length of ciphertext	
	"""
	sampleciphertext = encrypt_oracle('')
	plen = 1
	firstchange = 0
	secondchange = 0
	while True:
		ciphertext = encrypt_oracle('\x20' * plen)
		if len(sampleciphertext) != len(ciphertext):
			if firstchange == 0:
				firstchange = plen
			else:
				secondchange = plen
				print "[+] blocksize: " + str(secondchange - firstchange) 
				return secondchange - firstchange
			sampleciphertext = ciphertext
		plen += 1


def confirm_encrypt_ECB(encrypt_oracle, blocksize):
	"""
	In this challenge, we dont need this function
	"""
	key = make_random_string(blocksize)	
	plaintext = make_random_string(blocksize) * 2	
	ciphertext_b = encrypt_oracle(plaintext)
			
	if ciphertext_b[0:blocksize] != ciphertext_b[blocksize:blocksize*2]:
		raise Exception("The function encrypt_oracle is not using ECB")
	else:
		print "[+] The function encrypt_oracle is using ECB"


def calculate_length_of_random_prefix(blocksize):	
	"""
	We add postfix to random-prefix, then apply comfirm-encrypt-ECB technique
	"""
	for rplen in range(1, blocksize+1):
		rpfill = ' ' * ((blocksize - rplen) % blocksize)		
		duplicate = make_random_string(blocksize) * 2
		ciphertext = encrypt_oracle(rpfill + duplicate)
		blocks = re.findall('..' * blocksize, ciphertext.encode('hex'))
		for i in range(len(blocks)-1):			
			if blocks[i] == blocks[i+1]:
				print '[+] The function encrypt_oracle is using ECB'				
				return rplen + ((i - 1) * blocksize)



def need_append(string, blocksize):
	"""
	Append data to left of string 
	=> (size of newstring + 1) mod blocksize == 0
	"""
	needappend = blocksize - len(string) % blocksize - 1
	return needappend * '\x20'


def make_lbdict(data, blocksize, rplen):			
	"""
	Try append last bytes, encrypt and save to dict
	"""	
	lbdict = {}		
	for i in range(0, 256):		
		blockcipher = encrypt_oracle(data + chr(i))		
		lbdict[blockcipher[rplen:len(data)+rplen+1]] = i							
	return lbdict


def get_unknown_string(encrypt_oracle, blocksize, rplen):	
	"""
	Get UNKNOWN_STRING without base64 decode module 
	"""
	rpfill = '\x20' * (blocksize - rplen % blocksize)	
	knownstring = ''		
	while True:				
		needappend = rpfill + need_append(knownstring, blocksize)	
		data = needappend + knownstring			# data = random-prefix || rpfill || knownstring || knownstring-fill
		lbdict = make_lbdict(data, blocksize, rplen)	# encrypt_oracle( data || for-character || unknown-string )					
		samplecipher = encrypt_oracle(needappend)[rplen:len(data)+rplen+1]   # encrypt_oracle( data || unknown-string )			
		if samplecipher in lbdict:						
			knownstring += chr(lbdict[samplecipher])
		else:				
			return knownstring	
	return knownstring


if __name__ == '__main__':
	blocksize = get_block_size(encrypt_oracle)				
	rplen = calculate_length_of_random_prefix(blocksize)
	print "[+] len(RANDOM_PREFIX):", rplen	
	print '[+] Unknown string:\n\n' + get_unknown_string(encrypt_oracle, blocksize, rplen)