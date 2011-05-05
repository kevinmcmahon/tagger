#!/usr/bin/env python

'''
Usage: build_dict.py -o <output file> -s <stopwords file> <list of files>
'''

import collections
import getopt
import math
import pickle
import sys

from tagger import Reader, Stemmer


if __name__ == '__main__':

    try:
        options = getopt.getopt(sys.argv[1:], 'o:s:')
        output_file = options[0][0][1]
        stopwords_file = options[0][1][1]
        corpus = options[1]
    except:
        print(__doc__)
        exit(1)
    
    reader = Reader()
    stemmer = Stemmer()

    with open(stopwords_file, 'r') as f:
        stopwords = f.read().split()
    
    words = []
    
    for doc in corpus:
        with open(doc, 'r') as f:
            words += reader(f.read())

    words = map(stemmer, words)

    term_count = collections.Counter(words)
    total_count = len(list(term_count.elements()))

    dictionary = collections.defaultdict(int)
    
    for w in term_count:
        if w.stem in stopwords:
            dictionary[w.stem] = 0.0
        else:
            dictionary[w.stem] = 1.0 - \
                math.log(float(term_count[w]) + 1) / math.log(total_count)

    with open(output_file, 'w') as f:
        pickle.dump(dictionary, f)
        

