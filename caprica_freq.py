##Back to the Future IM Module
##Eric Mika + Michael Edgcumbe
##Learning Bit by Bit at NYU ITP, Spring 2010
 
 
import sys
import nltk
import string
import re
from nltk import FreqDist
from nltk.corpus import wordnet
from nltk import pos_tag
from nltk.collocations import *
from nltk import *
import random
 
## CREATE A CLASS TO HOLD THE IM DATA
class Line:
	## class holds the chat data, lookup is a list of synonyms	 
	def __init__(self,i,a,l,d):
		self.id = i
		self.author = a
		self.words = l
		self.lookup = list()
		self.index = d


## READ IN AND STORE THE IM TEXT
file = open("edgwired_clean.txt")
rawEdg = file.readlines()
 
file = open("../obrigado_aim_clean.txt")
rawMika = file.readlines()
 
##file = open("allwords.txt")
##allwords = file.read()
 
## create a new list to hold the chat data
edgwired = list()
obrigado = list()
	
 
 
## PARSE THE DATA
def masticator(rawlog):
	digestedlist = list()
	index = 0
	for row in rawlog:
		## remove the \n
		row = row.strip()
		## split on the first 3 commas
		parseString = row.split(',',3)
 
		## store in variables and append to the chat list
		conversation_id = parseString[0]
		time = parseString[1]
		author = parseString[2]
		words = parseString[3]
 
		digestedlist.append(Line(conversation_id,author,words, index))
		index += 1
 
	return digestedlist
 
 
 
edgwired_log = masticator(rawEdg)
#obrigado_log = masticator(rawMika)

#edgwired_allText = ""
edgwired_allText = ""

for line in edgwired_log:
	edgwired_allText += line.words + " "

edgwired_tokens = nltk.word_tokenize(edgwired_allText)

i
fdist1 = FreqDist(edgwired_tokens)

text = nltk.Text(edgwired_tokens);
# bigrams = bigrams(edgwired_tokens)
# 
# print bigrams


bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
finder = BigramCollocationFinder.from_words(edgwired_tokens)

finder.apply_word_filter(lambda w: w in ('!','\'','"','#','$','%','&','(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[',']','^','_','`','{','|','}','~'))
finder.apply_word_filter(lambda w: w in ('1', '2', '3', '4','5','6','7','8','9','0'))

finder.apply_freq_filter(2)

for ngram in finder.ngram_fd.items():
	if ngram[1] > 1:
		the_gram = ngram[0][0] + " " + ngram[0][1]
		the_gram = the_gram.replace(",", "")
		print the_gram + "," + str(ngram[1])

	

#print finder.nbest(bigram_measures.pmi, 100)  

#unusual_pairs = text.collocations()
#print unusual_pairs


# for value in fdist1.items():
# 	print str(value[0]) + "," + str(value[1])
	

# for token, count in fdist1:
# 	print count

# print vocab

# for line in obrigado_log:
# 	pass