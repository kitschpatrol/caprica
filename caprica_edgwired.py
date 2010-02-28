import sys
import nltk
import re
from nltk.corpus import wordnet
import random

chat = list()


one = ["one", "two"]
two = ["three"]

one.extend(two)
print one

class Line:
  def __init__(self, i, a, l):
	self.id = i
	self.author = a
	self.words = l
	self.lookup = list()

	templookup = self.words.split(" ")

	for word in templookup:
		sense_list = wordnet.synsets(word)
		if sense_list:
			self.lookup.append(sense_list[0].lemma_names)
		else:
			self.lookup.append([word])
			

testLine = Line(1,"eric","hello michael how are things")

##
##
##
##file = open("edgwired_clean.txt")
##text = file.readlines()
##
##
##for row in text:
##	try:
##	  row = row.strip()
##	  parseString = row.split(',',3)
##	  
##	  IDN = parseString[0]
##	  time = parseString[1]
##	  author = parseString[2]
##	  words = parseString[3]
##
##	  chat.append(Line(IDN,author,words))
##	  
##	except:
##	  break
##
####print len(chat)
####print chat[-1].author
####print chat[-1].words
