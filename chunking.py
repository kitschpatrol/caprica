##Back to the Future IM Module
##Eric Mika + Michael Edgcumbe
##Learning Bit by Bit at NYU ITP, Spring 2010

## Suggested Improvements:

##synonym/ DONE
##n-gram/  DONE
##question+response
##flagged
##original word/
##length of response/
##porter stemming/
##variations/
##dictionary/


import sys
import nltk
import re
from nltk.corpus import wordnet
from nltk.collocations import *
import random

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

## CREATE A CLASS TO HOLD THE IM DATA
class Line:
    ## class holds the chat data, lookup is a list of synonyms   
    def __init__(self,i,a,l):
        self.id = i
        self.author = a
        self.words = l
        self.lookup = list()        

def expand_words(words):
	## tokenize the list of words
	templookup = words.split(" ")
	
	lookup = list()
	
	for word in templookup:
	    ## for each word in the split list, create a new list which holds the synonyms
	    sense_list = wordnet.syssets(word)
	    
		if sense_list:
	        i = 0
	        templist = list()
	        for sense in sense_list:
	            templist.extend(sense_list[i].lemma_names)
	            i+=1
	        ## append the synonyms to the lookup list of words for the sentence
	        lookup.append(templist)
	    else:
	        ## if there are no synonyms, append the word used as the search term
	        lookup.append([word])
		
	return lookup
	
	
	
	


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

def masticator(rawlog):
    digestedlist = list()
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

        digestedlist.append(Line(conversation_id,author,words))

    return digestedlist

edgwired = masticator(rawEdg)
obrigado = masticator(rawMika)

print edgwired[0]
print obrigado[0]

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

