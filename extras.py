from tagger import Reader, Stemmer


class HTMLReader(Reader):
    '''
    A Reader subclass that also strips HTML code from the input
    '''

    def __call__(self, html):
        # alternative to test: http://bit.ly/jX50oE
        
        from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

        text = ''.join(BeautifulSoup(html).findAll(text=True))

        # map html entities
        text = BeautifulStoneSoup(text, convertEntities=
                                  BeautifulStoneSoup.HTML_ENTITIES)
        
        return Reader.__call__(self, text)
    

class NLTKStemmer(Stemmer):
    '''
    A Stemmer subclass that uses NLTK's implementation of the Porter stemming
    algorithm.
    '''

    def __init__(self):
        import nltk

        self.stemmer = nltk.stem.porter.PorterStemmer()
    
    def __call__(self, tag):
        stem = self.pre_stem(tag.string)
        tag.stem = self.stemmer.stem(tag.stem)
        return tag
        
