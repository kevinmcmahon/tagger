======
tagger
======

Module for extracting tags from text documents.
                   
Copyright (C) 2011 by Alessandro Presta

Configuration
=============

Dependencies:
python2.7, stemming, nltk (optional), lxml (optional), tkinter (optional)

You can install the stemming package with::

    $ easy_install stemming

Usage
=====

Tagging a text document from Python::

    import tagger
    weights = pickle.load(open('data/dict.pkl', 'rb')) # or your own dictionary
    myreader = tagger.Reader() # or your own reader class
    mystemmer = tagger.Stemmer() # or your own stemmer class
    myrater = tagger.Rater(weights) # or your own... (you got the idea)
    mytagger = Tagger(myreader, mystemmer, myrater)
    best_3_tags = mytagger(text_string, 3)

Running the module as a script::

    $ ./tagger.py <text document(s) to tag>

Example::

    $ ./tagger.py tests/*
    Loading dictionary... 
    Tags for  tests/bbc1.txt :
    ['bin laden', 'obama', 'pakistan', 'killed', 'raid']
    Tags for  tests/bbc2.txt :
    ['jo yeates', 'bristol', 'vincent tabak', 'murder', 'strangled']
    Tags for  tests/bbc3.txt :
    ['snp', 'party', 'election', 'scottish', 'labour']
    Tags for  tests/guardian1.txt :
    ['bin laden', 'al-qaida', 'killed', 'pakistan', 'al-fawwaz']
    Tags for  tests/guardian2.txt :
    ['clegg', 'tory', 'lib dem', 'party', 'coalition']
    Tags for  tests/post1.txt :
    ['sony', 'stolen', 'playstation network', 'hacker attack', 'lawsuit']
    Tags for  tests/wikipedia1.txt :
    ['universe', 'anthropic principle', 'observed', 'cosmological', 'theory']
    Tags for  tests/wikipedia2.txt :
    ['beetroot', 'beet', 'betaine', 'blood pressure', 'dietary nitrate']
