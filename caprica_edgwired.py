import sys
import nltk
import re
from nltk.corpus import wordnet
import random

chat = list()

class Line:
  def __init__(self, a, l):
    self.author = a
    self.words = l

file = open("edgwired_clean.txt")
text = file.readlines()


for row in text:
  try:
    row = row.strip()
    parseString = row.split(',',3)
    
    IDN = parseString[0]
    time = parseString[1]
    author = parseString[2]
    words = parseString[3]

    chat.append(Line(author,words))
    
  except:
    break

##print len(chat)
##print chat[-1].author
##print chat[-1].words
