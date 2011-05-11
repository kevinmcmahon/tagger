#!/usr/bin/env python

from Tkinter import *
import tkMessageBox
import ScrolledText

from tagger import *
from extras import UnicodeReader

import pickle

with open('data/dict.pkl', 'rb') as f:
   weights = pickle.load(f)
tagger = Tagger(UnicodeReader(), Stemmer(), Rater(weights))

top = Tk()
top.title('tagger')

st = ScrolledText.ScrolledText(top)
st.pack()

def tag():
   tags = tagger(st.get(1.0, END))
   output = ', '.join(t.string for t in tags)
   tkMessageBox.showinfo('Tags:', output)
   st.delete(1.0, END)

b = Button(top, text ='TAG!', command=tag)

b.pack()
top.mainloop()
