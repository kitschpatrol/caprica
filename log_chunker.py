# Chunks together lines of conversation (from an arg1 file)
import sys

source_text = sys.argv[1]
#source_text = "../obrigado_clean.txt"

file = open(source_text)
log = file.readlines()

last_author = ""
last_id = 0
line = 0
 
for row in log:
  # remove the \n
  row = row.strip()
  
  # split on the first 3 commas
  parseString = row.split(',',3)

  # store in variables and append to the chat list
  id = parseString[0]
  time = parseString[1]
  author = parseString[2]
  words = parseString[3]
  
  if (author in last_author) and (id == last_id):
    # the comma prevents a newline
    print "... " + words,
  else:
    # line break
    if line > 0: print
    print str(id) + "," + str(time) + "," + author + "," + words,
    
  last_author = author
  last_id = id
  line += 1