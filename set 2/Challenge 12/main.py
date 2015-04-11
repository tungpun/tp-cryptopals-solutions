#!/usr/bin/env python2.7
# This source code is my answer for challenge at http://cryptopals.com/sets/1/challenges/12/
# TODO: key -> blocksize

import hashlib
import base64
from Crypto.Cipher import AES
from Crypto import Random
from random import randint


UNKNOWN_STRING = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

UNKNOWN_KEY = "WDs9Vj1XRS9GLTJPMDNPUg=="


def encrypt_oracle(plaintext):		
	"""
	In realistic challenges, everything in this function is secret..... ignore it :D
	"""	
	key = base64.b64decode(UNKNOWN_KEY)	
	blocksize = 16		
	plaintext = PKCS7_padding(plaintext + base64.b64decode(UNKNOWN_STRING), blocksize)	
	aesobj = AES.new(key, AES.MODE_ECB)
	ciphertext = aesobj.encrypt(plaintext)	
	return ciphertext
	return base64.b64encode(ciphertext)


def PKCS7_padding(text, blocksize):		
	needappend = blocksize - len(text) % blocksize
	return (text + '\x20' * needappend)	


def make_random_key(keylength):
	start = ord('\x20')
	end = ord('z')	
	key = ""
	for i in range(0, keylength):
		key += chr(randint(start, end+1))
	return key


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
				print "[+] Found! blocksize: " + str(secondchange - firstchange) 
				return secondchange - firstchange
			sampleciphertext = ciphertext
		plen += 1


def confirm_encrypt_ECB(encrypt_oracle, blocksize):
	key = make_random_key(blocksize)	
	plaintext = make_random_key(blocksize) * 2	
	ciphertext_b = encrypt_oracle(plaintext)
			
	if ciphertext_b[0:blocksize] != ciphertext_b[blocksize:blocksize*2]:
		raise Exception("The function encrypt_oracle is not using ECB")
	else:
		print "[+] The function encrypt_oracle is using ECB"


def need_append(string, blocksize):
	"""
	Append data to left of string 
	=> (size of newstring + 1) mod blocksize == 0
	"""
	needappend = blocksize - len(string) % blocksize - 1
	return needappend * '\x20'


def make_lbdict(data, blocksize):			
	"""
	Try append last bytes, encrypt and save to dict
	"""
	lbdict = {}		
	for i in range(0, 256):		
		blockcipher = encrypt_oracle(data + chr(i))
		lbdict[blockcipher[0:len(data)+1]] = i							
	return lbdict


def get_unknown_string(encrypt_oracle, blocksize):	
	"""
	Get UNKNOWN_STRING without base64 decode module 
	"""
	knownstring = ''		
	while True:				
		needappend = need_append(knownstring, blocksize)	
		data = needappend + knownstring				
		lbdict = make_lbdict(data, blocksize)	# encrypt_oracle( data || for-character || unknown-string )			
		samplecipher = encrypt_oracle(needappend)[0:len(data)+1]   # encrypt_oracle( data || unknown-string )			
		if samplecipher in lbdict:			
			rc = chr(lbdict[samplecipher])					
			knownstring += rc
		else:				
			return knownstring	
	return knownstring


if __name__ == '__main__':
	blocksize = get_block_size(encrypt_oracle)	
	confirm_encrypt_ECB(encrypt_oracle, blocksize)	
	print '[+] Unknown string:\n\n' + get_unknown_string(encrypt_oracle, blocksize)