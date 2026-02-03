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
		self.synonymscore = 0
		self.ngramscore = 0
 
def expand_words(words):
	## tokenize the list of words
	templookup = words.split(" ")
 
	lookup = list()
 
	for word in templookup:
		## for each word in the split list, create a new list which holds the synonyms
		sense_list = wordnet.synsets(word)
 
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
##file = open("edgwired.txt")
##rawEdg = file.readlines()
 
file = open("../obrigado.txt")
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
                        message.synonymscore += 1
                        hits.append(message)
                        
        hitMax = len(hits)
 
        #Find the unique hits
        for i in range(1,hitMax):
            if hits[i-1].index != hits[i].index:
                uniqueHits.append(hits[i])


        print uniqueHits[0].synonymscore
        return uniqueHits
            
 
 
##RANK THE MATCHES
def rank_ngrams(current_speaker, query, possibilities):

    query_tokens = nltk.wordpunct_tokenize(query.words)
    query.ngrams = BigramCollocationFinder.from_words(query_tokens)
    query_score = query.ngrams.score_ngrams(bigram_measures.jaccard)
    query_sort = sorted(bigram for bigram, score in query_score)
    
    for message in possibilities:
            
        tokens = nltk.wordpunct_tokenize(message.words)
        if message.id == "575":
            print tokens
        message.ngrams = BigramCollocationFinder.from_words(tokens)
        ngram_score = message.ngrams.score_ngrams(bigram_measures.jaccard)
        ngram_sort = sorted(bigram for bigram, score in ngram_score)

    for message in possibilities:
        ngram_score = message.ngrams.score_ngrams(bigram_measures.jaccard)
        ngram_sort = sorted(bigram for bigram, score in ngram_score)
        if message.id == "575":
            print message.words
        for ngram in query_sort:
            for thing in ngram_sort:
                    
                thing_0 = thing[0].lower()
                thing_1 = thing[1].lower()
                ngram_0 = ngram[0].lower()
                ngram_1 = ngram[1].lower()
                    
                if thing_0 == ngram_0 and thing_1 == ngram_1:
                    message.ngramscore +=1
                    print thing
                    print message.author
                    print "MESSAGE ID:"
                    print message.id
                    print "NGRAM SCORE:"
                    print message.ngramscore
                    print message.words
                    print " "

  
##bigram_finder = BigramCollocationFinder.from_words(allwords_tokens)
##bigram_scored = bigram_finder.score_ngrams(bigram_measures.raw_freq)
##
##trigram_finder = TrigramCollocationFinder.from_words(allwords_tokens)
##trigram_scored = trigram_finder.score_ngrams(trigram_measures.raw_freq)
 
## SORT: sorted(bigram_finder.nbest(bigram_measures.raw_freq,10)
## FILTER BY FREQUENCY: bigram_finder.apply_freq_filter(5)
## FIND LENGTH: len(bigram_finder.score_ngrams(bigram_measures.raw_freq))
            
 
 
#edgwired = masticator(rawEdg)
obrigado = masticator(rawMika)
 
i_say = "just leave me alone girl"
#i_say = sys.argv[1]
my_name = "edgewired"
prime_query = Line(0,my_name,i_say,0)
prime_query.lookup = expand_words(prime_query.words)
 
query = prime_query
possibilities = search(prime_query,edgwired)   #returns a list of line objects that have matched words or synonyms
 
 
print len(possibilities)
rank_ngrams("Obrigado",prime_query,possibilities)
 
 
if "obrigado" in my_name:
    my_name = "edgwired"
else:
    my_name = "obrigado"
 
 
 
 
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
