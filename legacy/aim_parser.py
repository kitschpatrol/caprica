# Converts my aim logs to our special format
# CHATID,DATE,AUTHOR,CHAT
import re
import time
			
file = open("../aim.txt")
aim_log = file.readlines()

#Sessions demarcated with either of the followug:
#Session Start (obrigado:ollHONDAllo): Tue Mar 30 16:22:16 2004
#Session Close (ollHONDAllo): Tue Mar 30 16:26:09 2004

#Start of ollHONDAllo buffer: Sat Sep 29 02:07:00 2001
#End of ollHONDAllo buffer: Sat Sep 29 02:14:02 2001

my_username = "obrigado"
chat_id = 0
unix_time= 0.0

#find the conversation bounds
for line in aim_log:
	# Remove endline and white space
	line = line.strip()

	# Make sure it's a reasonable line and not meta-cruft	
	if len(line) > 0 and not re.match("^\*", line) and not re.match("^-", line):
		# Look for conversation start
		if re.match("^Start of", line) or re.match("^Session Start", line):
			chat_id += 1;
			# extract the date, comes in as Sep 29 02:14:02 2001	
			# would be better to infer each date as a point between
			# session start and close... maybe if we actually use the data
			time_string = line[len(line) - 20:len(line)]
			python_time = time.strptime(time_string,"%b %d %H:%M:%S %Y")
			unix_time = time.mktime(python_time)

		# Look for conversation end
		elif re.match("^End of", line) or re.match("^Session Close", line):
			# Do something at session end, if we want
			pass

		# Must be a line of conversation
		else:
			# Split off the author from the text
			expanded_line = line.split(":", 1)

			# Sometimes new lines within a chat mess this up, make sure
			# it's a legitimate colon-laded line, otherwise just drop it.
			if len(expanded_line) > 1:
				author = expanded_line[0]
				text = expanded_line[1].strip()

				# Anonymize the author if it's not me.
				if not re.match(my_username, author, re.IGNORECASE):
					author = "other"
					
				print str(chat_id) + "," + str(unix_time) + "," + author.lower() + "," + text