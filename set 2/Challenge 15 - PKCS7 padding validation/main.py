#!/usr/bin/env python2.7
# This source code is my answer for challenge at http://cryptopals.com/sets/2/challenges/15/

import hashlib
import base64
import re
from Crypto.Cipher import AES
from Crypto import Random
from random import randint


def first_special_character_position(plaintext):
	for i in range(0, len(plaintext)):
		if ord(plaintext[i]) <= 8:			
			return i


def is_pkcs7_padding(plaintext):
	n = len(plaintext)
	fp = first_special_character_position(plaintext)
	padlen = n - fp	
	for i in range(fp, n):
		if ord(plaintext[i]) != padlen:
			return False
	return True


if __name__ == '__main__':
	plaintext = "ICE ICE BABY\x06\x06\x06\x06\x06\x06"
	print is_pkcs7_padding(plaintext)