#!/usr/bin/env python2.7
# This source code is my answer for challenge at http:#cryptopals.com/sets/3/challenges/23
# Follow pseudo code at http://en.wikipedia.org/wiki/Mersenne_Twister

from Crypto.Random import random

SECRETSEED = 1233
MTSIZE = 624

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


def untemper(y):                
    def undo_right_shift_xor(y, shiftlen):
        def get_MSB(x, i):
            if i < 0:
                return 0
            return (x >> (31 - i)) & 1

        def set_MSB(x, i, value):
            return x | (value << (31 - i))

        z = 0
        for i in range(32):
            z = set_MSB(z, i, get_MSB(y, i) ^ get_MSB(z, i - shiftlen))
        return z

    def undo_left_shift_xor_and(y, shiftlen, magicnumber):
        def get_LSB(x, i):
            if i < 0:
                return 0
            return (x >> i) & 1

        def set_LSB(x, i, value):
            return x | (value << i)

        z = 0
        for i in range(32):
           z = set_LSB(z, i, get_LSB(y, i) ^ (get_LSB(z, i - shiftlen) & get_LSB(magicnumber, i)))
        return z

    y = undo_right_shift_xor(y, 18)
    y = undo_left_shift_xor_and(y, 15, 0xefc60000)
    y = undo_left_shift_xor_and(y, 7, 0x9d2c5680)
    y = undo_right_shift_xor(y, 11)
    return y


def get_MT(rng):        
    MT = [0] * MTSIZE
    for i in range(MTSIZE):        
        MT[i] = untemper(rng.extract_number())
    return MT


def compare_rng(rng1, rng2):    
    for i in range(1000):
        if rng.extract_number() != cloned_rng.extract_number():
            return False    # Clone Failed
    return True


if __name__ == '__main__':
    seed = random.randint(0, 10000000)
    rng = MT19937RNG(seed)
    cloned_rng = MT19937RNG(0)
    cloned_rng.MT = get_MT(rng)
    print compare_rng(rng, cloned_rng)