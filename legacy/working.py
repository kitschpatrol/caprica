import sys
import nltk
import re
from nltk.corpus import wordnet
import random
import string
 
chat = list()
# http://tartarus.org/~martin/PorterStemmer/
def lowerStrings(word_list):
	return [x.lower() for x in word_list]
	
def expand_words(words):
	## tokenize the list of words
	templookup = words.split(" ")
	uniqueLookup = list() 
 
	lookup = list()
 
	for word in templookup:
		## for each word in the split list, create a new list which holds the synonyms
		sense_list = wordnet.synsets(word)
 
		if sense_list:
			i = 0
			templist = list()
			for sense in sense_list:
				templist.extend(lowerStrings(sense_list[i].lemma_names))
				i+=1
			## append the synonyms to the lookup list of words for the sentence
			lookup.append(templist)
		else:
			## if there are no synonyms, append the word used as the search term
			lookup.append([word])

	# remove duplicates
	for synonyms in lookup:
		uniqueLookup = synonyms
		#uniqueLookup.append([x for x in synonyms if x not in locals()[1]])

	return uniqueLookup

 
class Line:
	def __init__(self, i, a, l):
		self.id = i
		self.author = a
		self.words = l
		self.lookup = list()
 
	def expand_words(self):
		self.lookup = expand_words(self.words)
 
# query_line = Line(1,"eric","meaning of life")
# query_line.expand_words()
# 
# print query_line.lookup
 
 
 
#query_line = Line(1,"eric","hello michael how are things")
#query_line = Line(1, "michael","i am not in love with this corpus")
 
 
file = open("obrigado.txt")
text = file.readlines()
 
 
 
for row in text:
	row = row.strip()
	parseString = row.split(',',3)
 
	conversation_id = parseString[0]
	time = parseString[1]
	author = parseString[2]
	words = parseString[3]
 
	chat.append(Line(conversation_id, author, words))
 
 
 
 
# This is crude. It gives the line of some other's text
# with the most instances of the synonyms in our query string
def ask_something(you_ask):
 
	query_line = Line(1,"eric", you_ask)
	query_line.expand_words()
 
	row_index = 0
	best_fit = 0
	best_index = 0
 
	#print query_line.lookup

	for chat_line in chat:
 
		if "obrigado" not in chat_line.author:
 
			fit = 0
 
			for synonyms in query_line.lookup:
				for word in synonyms:
					if word in chat_line.words:
						fit += 1
			#print "line " + str(row_index) + " has fit of " + str(fit)
			# change to a >= to give us older michael
			# this is a problem, if we have a bunch of matches
			# we need some kind of round 2 filter to pick the
			# very best one and break the tie
			if fit > best_fit:
				# uncomment to print top candidates
				# print "Score: " + str(fit) + " " + chat_line.author + ": " + chat_line.words		
				best_index = row_index
				best_fit = fit
 
		row_index += 1
 
	#print best_fit
	#print chat[best_index].words
 
	# Now let's start at the chat line that best fit our query string,
	# and then walk forward through the log to Michael's response
 
	# also need to factor chat boundaries
	for chat_line in chat[best_index:len(chat)]:
 
		#print chat_line.author + ": " + chat_line.words		
		if "obrigado" in chat_line.author:
			return chat_line.author + ": " + chat_line.words
			break
 
 
 
 
# print ask_something("meaning of life");
 
while 1:
 
	you_say = raw_input("You say: ")
 
	if you_say == "quit":
		break
	else:
		print ask_something(you_say)
 
 
##print len(chat)
##print chat[-1].author
##print chat[-1].words