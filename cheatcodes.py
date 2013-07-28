#!/usr/bin/env python

from __future__ import division

import bisect
import gzip
import hashlib
import math
import os
import re
import sys

INPUT_BITS = 160
WORDS_DESIRED = 11
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

    assert len(words) == WORDS_NEEDED
    words.sort()
    return words


def encode(words, h):
    output = []
    while h:
        h, idx = divmod(h, len(words))
        output.append(words[idx])
    return output


def indexOf(words, word):
    idx = bisect.bisect_left(words, word)
    assert words[idx] == word
    return idx


def decode(words, code):
    h = 0
    for word in reversed(code):
        h = (h * len(words)) + indexOf(words, word)
    return h


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

    elif sys.argv[1] == 'decode':
        h = decode(words, sys.argv[2:])
        s = '%x' % h
        print
        print s, '=', ' '.join(sys.argv[2:])
        print


if __name__ == '__main__':
    main()
