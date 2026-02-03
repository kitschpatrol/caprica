##Back to the Future IM Module
##Eric Mika + Michael Edgcumbe
##Learning Bit by Bit at NYU ITP, Spring 2010
 
## Suggested Improvements:
 
##synonym/ DONE
##n-gram/	 DONE
##question+response
##flagged
##original word/
##length of response/
##porter stemming/
##variations/
##dictionary/
 
 
import sys
import nltk
import string
import re
from nltk.corpus import wordnet
from nltk import pos_tag
##from nltk.corpus import brown
##from nltk.corpus import nps_chat
from nltk.collocations import *
import random
 
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
 
## CREATE A CLASS TO HOLD THE IM DATA
class Line:
	## class holds the chat data, lookup is a list of synonyms	 
	def __init__(self,i,a,l,d):
		self.id = i
		self.author = a
		self.words = l
		self.lookup = list()
		self.index = d
		self.ngrams = list()
		self.synonymscore = float(0)
		self.ngramscore = 0
		self.used = 0

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
		for synonym in synonyms:
			if synonym not in uniqueLookup:
				uniqueLookup.append(synonyms)

	return uniqueLookup
 
## READ IN AND STORE THE IM TEXT
file = open("edgwired_clean.txt")
rawEdg = file.readlines()
 
file = open("../obrigado_clean.txt")
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
 
 
## SEARCH THE DATA
def search(query, bank):
				hits = list()
				uniqueHits = list()
 
				#Find the matches between synonyms
				for message in bank:
						for synlists in query.lookup:
								for synonym in synlists:
										if synonym in message.words:
												message.synonymscore += 1.0
												hits.append(message)
 
				hitMax = len(hits)
##				print hitMax
 
				#Find the unique hits
				for i in range(1,hitMax):
						if hits[i-1].index != hits[i].index:
								uniqueHits.append(hits[i])
 
##				print len(uniqueHits
##				for i in range(10):
##						print uniqueHits[i].words

				for hit in uniqueHits:
					hit.synonymscore = hit.synonymscore / (float(len(hit.words.split(" "))))
					#print "ID: " + str(hit.id) + " Score:" + str(hit.synonymscore)
					
				
				
				return uniqueHits

 
 
##RANK THE MATCHES
def rank_ngrams(query, possibilities):

	query_tokens = nltk.wordpunct_tokenize(query.words)
	query.ngrams = BigramCollocationFinder.from_words(query_tokens)
	query_score = query.ngrams.score_ngrams(bigram_measures.jaccard)
	query_sort = sorted(bigram for bigram, score in query_score)

	for message in possibilities:

		tokens = nltk.wordpunct_tokenize(message.words)
		message.ngrams = BigramCollocationFinder.from_words(tokens)
		ngram_score = message.ngrams.score_ngrams(bigram_measures.jaccard)
		ngram_sort = sorted(bigram for bigram, score in ngram_score)

	for message in possibilities:
		ngram_score = message.ngrams.score_ngrams(bigram_measures.jaccard)
		ngram_sort = sorted(bigram for bigram, score in ngram_score)
		for ngram in query_sort:
			for thing in ngram_sort:

				thing_0 = thing[0].lower()
				thing_1 = thing[1].lower()
				ngram_0 = ngram[0].lower()
				ngram_1 = ngram[1].lower()


				if thing_0 == ngram_0 and thing_1 == ngram_1 and (thing_0 not in string.punctuation) and (thing_0 not in string.punctuation):
					message.ngramscore +=1
					print thing
					print message.author
					print "MESSAGE ID:"
					print message.id
					print "NGRAM SCORE:"
					print message.ngramscore
					print message.words
					print " "
					
	return possibilities


##bigram_finder = BigramCollocationFinder.from_words(allwords_tokens)
##bigram_scored = bigram_finder.score_ngrams(bigram_measures.raw_freq)
##
##trigram_finder = TrigramCollocationFinder.from_words(allwords_tokens)
##trigram_scored = trigram_finder.score_ngrams(trigram_measures.raw_freq)
 
## SORT: sorted(bigram_finder.nbest(bigram_measures.raw_freq,10)
## FILTER BY FREQUENCY: bigram_finder.apply_freq_filter(5)
## FIND LENGTH: len(bigram_finder.score_ngrams(bigram_measures.raw_freq))
						
 
 
edgwired_log = masticator(rawEdg)
obrigado_log = masticator(rawMika)


def get_response(question, response_log):

	# build the query line
	query = Line(0,"whatever",question,0)

	# build the synonyms
	query.lookup = expand_words(query.words)

	# find the possible responses
	possible_responses = search(query, response_log)
	
	# consider ngram matches : (
	#rank_ngrams(query, possible_responses);
	
	# rank the responses
	high_score = 0
	for line in possible_responses:
		if line.synonymscore > high_score: high_score = line.synonymscore
	#print high_score
	
	# choose a high scoring response
	match_index = 0
	for line in possible_responses:
		if (line.synonymscore == high_score):
			#print line.index
			match_index = line.index

	# walk forward to the first response
	
	# mark it as used
	# response_log[response_index].used = 1
	
	match = response_log[match_index]
	response = ""

	
	for line in response_log[match_index:len(response_log)]:
		if (line.author.lower() != "other") and (line.used != 1):
			response_log[line.index].used = 1
			response = line
			break

	# # include your own responses
	# for line in response_log[match_index:len(response_log)]:
	# 	if (line.used != 1):
	# 		response_log[line.index].used = 1
	# 		response = line
	# 		break	
	
	# return one
	return response;	




def chooseLog(asker_name):
	if asker == "eric":
		return edgwired_log
	else:
		return obrigado_log
 

# Main loop
# Automatic mode
# asker = "eric"
# query = "pics"
# while 1 == 1:
#     response = get_response(query, chooseLog(asker))
# 
#     # print some conversation
#     #print response.synonymscore
#     print response.author + ": " + response.words
#     
#     # flip the asker
#     if asker == "eric":
#         asker = "michael"
#     else:
#         asker = "eric"
#     
#     # load the query
#     query = response.words    

# interactive mode
asker = "michael"
while 1:
    you_say = raw_input("You say: ")
 
    if you_say == "quit":
        break
    else:
        response = get_response(you_say, chooseLog(asker))
        print response.author + ": " + response.words









#rank_ngrams("Obrigado",prime_query,possibilities)


 
 
# if "obrigado" in my_name:
#			my_name = "edgwired"
# else:
#			my_name = "obrigado"
 
 
 
 
#### CREATE BIGRAMS AND TRIGRAMS
##allwords_tokens = nltk.wordpunct_tokenize(allwords)
##
##bigram_finder = BigramCollocationFinder.from_words(allwords_tokens)
##bigram_scored = bigram_finder.score_ngrams(bigram_measures.raw_freq)
##
##trigram_finder = TrigramCollocationFinder.from_words(allwords_tokens)
##trigram_scored = trigram_finder.score_ngrams(trigram_measures.raw_freq)
 
## SORT: sorted(bigram_finder.nbest(bigram_measures.raw_freq,10)
## FILTER BY FREQUENCY: bigram_finder.apply_freq_filter(5)
## FIND LENGTH: len(bigram_finder.score_ngrams(bigram_measures.raw_freq))
 
 
##TAGGING
#nps_train = nltk.corpus.nps_chat.tagged_words('10-19-20s_706posts.xml')
#unigram_tagger = nltk.UnigramTagger(nps_train)
#bigram_tagger = nltk.BigramTagger(nps_train, backoff=unigram_tagger)
 
#brown_news_tagged = brown.tagged_sents(categories = 'news')
#tagger = nltk.UnigramTagger(brown_news_tagged)