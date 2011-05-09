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


from tagger import *


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

    
class SimpleReader(Reader):
    '''
    Reader subclass that doens't perform any advanced analysis of the text.
    '''
    
    def __call__(self, text):
        text = text.lower()
        text = self.match_punctuation.sub('\n', text)
        words = self.match_words.findall(text)
        tags = [Tag(w) for w in words]
        return tags


class FastStemmer(Stemmer):
    '''
    Stemmer subclass that uses a much faster, but less correct algorithm
    '''

    def __init__(self):
        from stemming import porter
        Stemmer.__init__(self, porter)


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


def build_dict_from_nltk(output_file, corpus=None, stopwords=None,
                         reader=SimpleReader(), stemmer=Stemmer(),
                         verbose=False):
    '''
    Arguments:

    output_file           --    the binary stream where the dictionary should
                                be saved
    corpus                --    the NLTK corpus to use (defaults to
                                nltk.corpus.brown)
    stopwords             --    a list of (not stemmed) stopwords (defaults to
                                nltk.corpus.stopwords.words('english'))
    reader                --    the Reader object to be used
    stemmer               --    the Stemmer object to be used
    verbose               --    whether information on the progress should be
                                printed on screen
    '''
    
    from build_dict import build_dict
    import nltk
    import pickle

    if not corpus:
        nltk.download('brown', quiet=True)
        corpus = nltk.corpus.brown

    if not stopwords:
        nltk.download('stopwords', quiet=True)
        stopwords = nltk.corpus.stopwords.words('english')

    # just for consistency
    if verbose: print 'Reading stopwords...'
    
    if verbose: print 'Reading corpus...'
    text = ' '.join(corpus.words())
    words = reader(text)

    if verbose: print 'Processing tags...'
    words = map(stemmer, words)
    stopwords = map(stemmer, (Tag(w) for w in stopwords))

    if verbose: print 'Building dictionary... '
    dictionary = build_dict([w.stem for w in words],
                            [w.stem for w in stopwords])

    if verbose: print 'Saving dictionary... '
    pickle.dump(dictionary, output_file, -1) 



    

    

     

    

        

    





        
