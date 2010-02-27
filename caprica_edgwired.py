
import sys
import nltk
import re
from nltk.corpus import wordnet
import random

# An object to store each line of conversation
class Line:
  """A line of text as said by a particular author."""
  def __init__(self, a, l):
    self.author = a
    self.words = l
  
  def formatted(self):
    """Returns the line as though it was formatted by aim."""
    return self.author + ": " + self.words


# Open the archives.
# Eventually this will search your disk for the log files.
file = open("Edgwired_messages_hail_mary.txt")


# Put each utterance into an object so we can easily separate the author from what
# he or she said.
lines = list()


for line in file:

  # Remove the newline characters.
  line = line.strip()
  
  # Make sure it's an actual line of conversation by checking for meta-lines.
##  if len(line) > 0 \
##  and ":" in line \
##  and not re.match("^Start", line) \
##  and not re.match("^Session", line) \
##  and not re.match("^\*", line) \
##  and not re.match("^-", line):
    # Well, it must be a real line of conversation.
    
    # Extract the author and line based on the position of the colon.
  parseString = line.split(',', 3)
  
  IDN = parseString[0]
  time = parseString[1]
  author = parseString[2]
  words = parseString[3]

  #print author + ": " + words
    
  # Add it to the list.
  lines.append(Line(author, words))


print "Searching " + str(len(lines)) + " lines of conversation."
  
# Now the data is structured...

# Better than the string search would be a way to find the most simialr sentence
# based on context / content.

# Find a response to what I say.
i_say = "why" # This should come in over stdin eventually.
i_say = sys.argv[1]
my_name = "Edgwired"
response_size = random.randint(1, 5) # How many lines to respond with. Prevents excessively terse responses.
print "you: " + i_say

still_looking = True
for i in range(len(lines)):
  line = lines[i]

  # First, look for an exact match to what I said
  
  if i_say in line.words:
    # Walk forward to my
    while (i < len(lines) - 1) and (still_looking or response_size > 0):
      i += 1
      possible_response = lines[i]
      if possible_response.author == my_name:
        print possible_response.formatted()
        response_size -= 1
        
        if response_size is 0:
          still_looking = False
          break
    
    if not still_looking:
      break

# Didn't find anyhting...
while response_size > 0:
  response_size -= 1
  print my_name + ": ..."
  








# for synset in wordnet.synsets("vehicle"):
#   print synset.lemma_names

