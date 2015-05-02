#!/usr/bin/env python2.7
# This source code is my answer for challenge at http://cryptopals.com/sets/1/challenges/24/

import hashlib
import base64
import re
from Crypto.Cipher import AES
from Crypto import Random
import random
import struct
import time

MTSIZE = 624


def make_random_string(keylength):
	start = ord('\x20')
	end = ord('z')	
	key = ""
	for i in range(0, keylength):
		key += chr(random.randint(start, end+1))
	return key


class MT19937RNG:
    # Initialize the generator from a seed
    def __init__(self, seed):    	
        self.MT = [0] * MTSIZE
        self.index = 0        
        self.MT[0] = seed & 0xffffffff     # We just play with lowest 32 bits of each element
        for i in range(1, 623+1): # loop over each element
            self.MT[i] = ((0x6c078965 * (self.MT[i-1] ^ (self.MT[i-1] >> 30))) + i) & 0xffffffff # We use "& 0xffffffff" to get lowest 32 bits of each element
        

    # Extract a tempered pseudorandom number based on the index-th value,
    # calling generate_numbers() every MTSIZE numbers
    def extract_number(self):
        if self.index == 0:
            self.generate_numbers()        
        y = self.MT[self.index]
        y = y ^ (y >> 11)
        y = y ^ ((y << 7) & (0x9d2c5680))
        y = y ^ ((y << 15) & (0xefc60000))
        y = y ^ (y >> 18)

        self.index = (self.index + 1) % MTSIZE
        return y


    # Generate an array of MTSIZE untempered numbers
    def generate_numbers(self):
        for i in range(MTSIZE):
            y = (self.MT[i] & 0x80000000) + (self.MT[(i+1) % MTSIZE] & 0x7fffffff)  
            self.MT[i] = self.MT[(i + 397) % MTSIZE] ^ (y >> 1)
            if (y % 2) != 0: # y is odd
                self.MT[i] = self.MT[i] ^ 0x9908b0df


class MT19937StreamCipher:
	def __init__(self, seed):

		def produce_keystream(seed, keylen):
			rng = MT19937RNG(seed)
			keystream = ''
			while len(keystream) < keylen:
				keystream += struct.pack('<L', rng.extract_number())				
			return keystream			
		self.keyStream = produce_keystream(seed, 1000)				


	def crypt(self, plaintext):
		def xor_rawtext(bigrawtext, rawtext):	
			res = ""		
			for i in range(len(rawtext)):
				res += chr(ord(bigrawtext[i]) ^ ord(rawtext[i]))
			return res

		if len(plaintext) > len(self.keyStream):
			raise Exception, "Length of keyStream is not enough for plaintext"
		return xor_rawtext(self.keyStream, plaintext)


def recover_key(sampleciphertext):
	startposofknowntext = len(sampleciphertext) - 16	
	for i in range(2**16-1):		
		cipher = MT19937StreamCipher(i)
		ciphertext = cipher.crypt('A' * len(sampleciphertext))	
		if ciphertext[startposofknowntext:] == sampleciphertext[startposofknowntext:]:
			return i
	return -1


def get_password_token():
	seed = int(time.time())
	cipher = MT19937StreamCipher(seed)	
	plaintext = 'A' * random.randint(4, 16)
	return cipher.crypt(plaintext)


def is_current_password_token(token):
	seed = int(time.time())
	cipher = MT19937StreamCipher(seed)	
	plaintext = 'A' * len(token)
	return cipher.crypt(plaintext) == token


if __name__ == '__main__':
	knowntext = 'A' * 16
	prefix = make_random_string(random.randint(4, 16))
	plaintext = prefix + knowntext
	secretkey = random.randint(0, 2**16-1)
	cipher = MT19937StreamCipher(secretkey)
	ciphertext = cipher.crypt(plaintext)
	print "Key:", recover_key(ciphertext)

	currentToken = get_password_token()
	print "Is current password token:", is_current_password_token(currentToken)