#!/usr/bin/env python2.7
# This source code is my answer for challenge at http:#cryptopals.com/sets/3/challenges/22
# Follow pseudo code at http://en.wikipedia.org/wiki/Mersenne_Twister

SECRETSEED = 1233

class MT19937RNG:
    # Initialize the generator from a seed
    def __init__(self, seed):
        self.MT = [0] * 624
        self.index = 0        
        self.MT[0] = seed & 0xffffffff     # We just play with lowest 32 bits of each element
        for i in range(1, 623+1): # loop over each element
            self.MT[i] = ((0x6c078965 * (self.MT[i-1] ^ (self.MT[i-1] >> 30))) + i) & 0xffffffff # We use "& 0xffffffff" to get lowest 32 bits of each element
        

    # Extract a tempered pseudorandom number based on the index-th value,
    # calling generate_numbers() every 624 numbers
    def extract_number(self):
        if self.index == 0:
            self.generate_numbers()

        y = self.MT[self.index]
        y = y ^ (y >> 11)
        y = y ^ ((y << 7) & (0x9d2c5680))
        y = y ^ ((y << 15) & (0xefc60000))
        y = y ^ (y >> 18)

        self.index = (self.index + 1) % 624
        return y


    # Generate an array of 624 untempered numbers
    def generate_numbers(self):
        for i in range(0, 623+1):
            y = (self.MT[i] & 0x80000000) + (self.MT[(i+1) % 624] & 0x7fffffff)  
            self.MT[i] = self.MT[(i + 397) % 624] ^ (y >> 1)
            if (y % 2) != 0: # y is odd
                self.MT[i] = self.MT[i] ^ 0x9908b0df


def get_seed(rnum):
    def make_seed_list():            
        seedlist = []
        for seed in range(2000):
            rng = MT19937RNG(seed)
            seedlist.append(rng.extract_number())
        return seedlist

    seedlist = make_seed_list()    
    for i in range(0, len(seedlist)):
        print '[+] Tested:', i
        if rnum == seedlist[i]:
            return i
    return -1

if __name__ == '__main__':
    rng = MT19937RNG(SECRETSEED)
    rnum = rng.extract_number()
    print get_seed(rnum)
    