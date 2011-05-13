#!/usr/bin/env python

# Copyright (C) 2011 by Alessandro Presta

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE


'''
Usage: build_dict.py -o <output file> -s <stopwords file> <list of files>
'''

from tagger import Stemmer
from extras import SimpleReader


def build_dict(corpus, stopwords=None, measure='IDF'):
    '''
    @param corpus:    a list of documents, represented as lists of (stemmed)
                      words
    @param stopwords: the list of (stemmed) words that should have zero weight
    @param measure:   the measure used to compute the weights ('IDF'
                      i.e. 'inverse document frequency' or 'ICF' i.e.
                      'inverse collection frequency'; defaults to 'IDF')

    @returns: a dictionary of weights in the interval [0,1]
    '''

    import collections
    import math

    dictionary = {}

    if measure == 'ICF':
        words = [w for doc in corpus for w in doc]
        
        term_count = collections.Counter(words)
        total_count = float(len(words))
        scale = math.log(total_count)
    
        for w, cnt in term_count.iteritems():
            dictionary[w] = math.log(total_count / (cnt + 1)) / scale

    elif measure == 'IDF':
        corpus_size = float(len(corpus))
        scale = math.log(corpus_size)

        term_count = collections.defaultdict(int)

        for doc in corpus:
            words = set(doc)
            for w in words:
                term_count[w] += 1

        for w, cnt in term_count.iteritems():
            dictionary[w] = math.log(corpus_size / (cnt + 1)) / scale
            
    if stopwords:
        for w in stopwords:
            dictionary[w] = 0.0
    
    return dictionary


def build_dict_from_files(output_file, corpus_files, stopwords_file=None,
                          reader=SimpleReader(), stemmer=Stemmer(),
                          measure='IDF', verbose=False):
    '''
    @param output_file:    the binary stream where the dictionary should be
                           saved
    @param corpus_files:   a list of streams with words to process
    @param stopwords_file: a stream containing a list of stopwords
    @param reader:         the L{Reader} object to be used
    @param stemmer:        the L{Stemmer} object to be used
    @param measure:        the measure used to compute the weights ('IDF'
                           i.e. 'inverse document frequency' or 'ICF' i.e.
                           'inverse collection frequency'; defaults to 'IDF')
    @param verbose:        whether information on the progress should be
                           printed on screen
    '''

    import pickle

    if verbose: print 'Processing corpus...'
    corpus = []
    for doc in corpus_files:
        corpus.append(reader(doc.read()))
    corpus = [[w.stem for w in map(stemmer, doc)] for doc in corpus]

    stopwords = None
    if stopwords_file:
        if verbose: print 'Processing stopwords...'
        stopwords = reader(stopwords_file.read())
        stopwords = [w.stem for w in map(stemmer, stopwords)]

    if verbose: print 'Building dictionary... '
    dictionary = build_dict(corpus, stopwords, measure)
    pickle.dump(dictionary, output_file, -1) 
    

if __name__ == '__main__':

    import getopt
    import sys
    
    try:
        options = getopt.getopt(sys.argv[1:], 'o:s:')
        output_file = options[0][0][1]
        stopwords_file = options[0][1][1]
        corpus = options[1]
    except:
        print __doc__
        exit(1)
    
    corpus = [open(doc, 'r') for doc in corpus]
    stopwords_file = open(stopwords_file, 'r')
    output_file = open(output_file, 'wb')

    build_dict_from_files(output_file, corpus, stopwords_file, verbose=True)

    output_file.close()
    stopwords_file.close()
    for doc in corpus:
        doc.close()
    
               

