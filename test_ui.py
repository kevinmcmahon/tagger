#!/usr/bin/env python

from Tkinter import *
import tkMessageBox
import ScrolledText
from tagger import *
import pickle

with open('data/dict.pkl', 'rb') as f:
   weights = pickle.load(f)
tagger = Tagger(Reader(), Stemmer(), Rater(weights))

top = Tk()
top.title('tagger')

st = ScrolledText.ScrolledText(top)
st.pack()

def tag():
   tags = tagger(st.get(1.0, END).encode('latin-1', 'ignore'))
   output = ', '.join(t.string for t in tags)
   tkMessageBox.showinfo('Tags:', output)
   st.delete(1.0, END)

B = Button(top, text ='TAG!', command=tag)

B.pack()
top.mainloop()
