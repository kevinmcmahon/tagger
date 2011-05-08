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


from tagger import Reader, Stemmer, Rater
from stemming import porter


class HTMLReader(Reader):
    '''
    Reader subclass that can parse HTML code from the input
    '''

    def __call__(self, html):
        # TODO: strip HTML code, map entities
        # tools: HTMLParser, htmlentitydefs, BeautifulSoup,
        # regular expressions
        
        #return Reader.__call__(self, text)
        pass


class NLTKStemmer(Stemmer):
    '''
    Stemmer subclass that uses NLTK's implementation of the Porter stemming
    algorithm
    '''

    def __init__(self):
        import nltk

        self.stemmer = nltk.stem.porter.PorterStemmer()
    
    def __call__(self, tag):
        stem = self.pre_stem(tag.string)
        tag.stem = self.stemmer.stem(stem)
        return tag


class FastStemmer(Stemmer):
    '''
    Stemmer subclass that uses a much faster, but less correct algorithm
    '''

    def __call__(self, tag):
        from stemming import porter
        
        stem = self.pre_stem(tag.string)
        tag.stem = porter.stem(stem)
        return tag


class CollocationsRater(Rater):
    '''
    Rater subclass that uses bigram and trigram collocations to identify
    significant multitags
    '''

    def __init__(weights, multitag_size=3):
        # there is no support for arbitrary length n-grams yet
        multitag_size = min(multitag_size, 3)
        
        Rater.__init__(self, multitag_size)
    
    def create_multitags(self, tags):
        # TODO
        # tools: nltk.collocations
        pass


# TODO: map/reduce implentation of dictionary building
# tools: Pool.map, couchdb, hadoop

     
# TODO: utilities to take advantage of nltk.corpus and nltk.text in dictionary
# building



        
