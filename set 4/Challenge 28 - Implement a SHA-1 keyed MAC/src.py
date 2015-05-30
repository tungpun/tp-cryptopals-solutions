#!/usr/bin/env python2.7
# This source code is my answer for challenge at http://cryptopals.com/sets/4/challenges/28

def SHA1(key, message):
	import hashlib
	_m = hashlib.sha1()
	_m.update(key + message)
	return _m.hexdigest()


if __name__ == '__main__':
	print SHA1('SALT@#$123', 'It is a super secret key')