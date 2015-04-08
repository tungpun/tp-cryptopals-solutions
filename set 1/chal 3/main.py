#!/usr/bin/env python2.7
# This source code is my answer for challange at http://cryptopals.com/sets/1/challenges/3/

import re

def main():
	s = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

	ss = re.findall('..', s)

	for key in range(ord('A'), ord('z')+1):
		res = ""
		for cc in ss:				
			i = int(cc, 16) ^ key			
			if ord('A') <= i <= ord('z'):
				res += chr(i)
		print res

if __name__ == '__main__':
	main()
