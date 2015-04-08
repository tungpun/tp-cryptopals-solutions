#!/usr/bin/env python2.7
# This source code is my answer for challange at http://cryptopals.com/sets/1/challenges/8/

import re

def main():	
	f = open("8.txt", "r")	
	data = f.read()
	f.close()		
		
	lines = data.split("\n")
	lineNum = 0
	for line in lines:
		lineNum += 1
		blocks = re.findall('.' * 8, line)	
		similarCnt = 0
		for fb in blocks:
			for sb in blocks:
				if fb == sb:
					similarCnt += 1
		print lineNum, similarCnt



if __name__ == '__main__':
	main()