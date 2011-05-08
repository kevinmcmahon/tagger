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

from tagger import Reader, Stemmer


def build_dict(words, stopwords=None):
    '''
    Arguments:

    words        --    the list of (stemmed) words used to build the dictionary
    stopwords    --    the list of (stemmed) words that should have zero weight

    Returns: a dictionary of IDF weights
    '''

    import collections
    import math

    term_count = collections.Counter(words)
    total_count = len(words)
    
    dictionary = {}
    
    for w, cnt in term_count.iteritems():
        dictionary[w] = 1.0 - math.log(float(cnt) + 1) / math.log(total_count)

    if stopwords:
        for w in stopwords:
            dictionary[w] = 0.0
    
    return dictionary


def build_dict_from_files(output_file, corpus, stopwords_file=None,
                          reader=Reader(), stemmer=Stemmer(), verbose=False):
    '''
    Arguments:

    output_file       --    the binary stream where the dictionary should be
                            saved
    corpus            --    a list of streams with words to process
    stopwords_file    --    a stream containing a list of stopwords
    reader            --    the Reader object to be used
    stemmer           --    the Stemmer object to be used
    verbose           --    whether information on the progress should be
                            printed on screen
    '''

    import pickle
    
    stopwords = None
    
    if stopwords_file:
        if verbose: print 'Reading stopwords...'
        stopwords = reader(stopwords_file.read())

    words = []
        
    print 'Reading corpus...'
    for doc in corpus:
        words += reader(doc.read())

    if verbose: print 'Processing tags...'
    words = map(stemmer, words)
    stopwords = map(stemmer, stopwords)

    if verbose: print 'Building dictionary... '
    dictionary = build_dict([w.stem for w in words],
                            [w.stem for w in stopwords])

    if verbose: print 'Saving dictionary... '
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
    
               

