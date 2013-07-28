#!/usr/bin/env python

import gzip
import hashlib
import math
import os
import re
import sys

INPUT_BITS = 160
WORDS_DESIRED = 11.
WORDS_NEEDED = math.ceil(2 ** (INPUT_BITS / WORDS_DESIRED))
WORDS_PATH = 'data/dict-%d.txt.gz' % (WORDS_NEEDED,)


def make_word_list():
    known = set(s.lower().strip() for s in open('data/words'))
    match = re.compile('^[A-Za-z]{3,}$').match
    vmatch = re.compile('[aeiouAEIOU]').search

    words = []
    for line in gzip.open('data/en.txt.gz'):
        word, freq = line.rstrip('\n').split(' ', 1)
        if match(word) and 'z' not in word and vmatch(word):
            if word not in known and word[:-1] not in known:
                continue
            words.append(word)
            if len(words) == WORDS_NEEDED:
                break

    words.sort()
    return words


def encode(words, h):
    hbits = INPUT_BITS
    per_word = math.floor(INPUT_BITS / WORDS_DESIRED)
    output = []
    n = 0
    bc = 0

    while hbits:
        n <<= 1
        n |= h & 1
        h >>= 1
        hbits -= 1
        bc += 1
        if bc == per_word:
            output.append(words[n])
            bc = 0
            n = 0

    if bc:
        output.append(words[n])

    return output


def main():
    if os.path.exists(WORDS_PATH):
        with gzip.open(WORDS_PATH) as fp:
            words = map(str.rstrip, fp)
    else:
        words = make_word_list()
        with gzip.open(WORDS_PATH, 'w') as fp:
            fp.writelines(word + '\n' for word in words)

    if sys.argv[1] == 'encode':
        try:
            s = sys.argv[2]
            h = int(s, 16)
        except ValueError:
            s = hashlib.sha1(sys.argv[2]).hexdigest()
            h = int(s, 16)

        print
        print s, '=', ' '.join(encode(words, h))
        print

if __name__ == '__main__':
    main()
