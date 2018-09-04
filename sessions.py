# Get the number of sessions and page views per session for a given SID
# where a session is the total page views within a 30 minute period.
# The input file has one row per page view so there will be many rows with
# the same SID.  The output file has only one row for each SID.
# Runtime for the full api log file of 500,000 rows is 4 minutes.

import pandas as pd
import sys  
from datetime import datetime


# Changed default string encoding from 'ascii' to 'utf8'
reload(sys)  
sys.setdefaultencoding('utf8')

# Input file
f = 'ftse.0510-0622.2018.api.logs_SAMPLE.csv'

# Read csv, remove empty rows and rows with null SID value
df = pd.read_csv(f, skiprows=None)
df = df.dropna(subset=['demandbase_sid'])
#df = df.head(200)

# Convert to datetime format
df['date_time'] =  pd.to_datetime(df['date_time'])


#---------------------------------------------------------------------------------------------

### GET NUMBER OF SESSIONS FOR EACH SID

def sessions(sid, datetime, session_time):

	session_counts = []

	# I Zipped the sid and datetime columns values together
	# pair[0] refers to sid, pair[1] refers to datetime for that sid
	sdt = zip(sid, datetime)

	for pair in sdt:

		# Case where SID is not in pageviews dictionary yet.
		if pair[0] not in pageviews.keys():
			pageviews[pair[0]] = [[pair[1]]]


		# SID will have 1 list of time values, or a list of lists of time values.
		# Compare datetime to the first element of the last list.
		else:

			initial_time = pageviews[pair[0]][-1][0]
			diff = pair[1] - initial_time
			diff = diff.seconds

			if diff <= session_time:

				pageviews[pair[0]][-1].append(pair[1])

			else:

				pageviews[pair[0]].append([pair[1]])

		session = len(pageviews[pair[0]])
		session_counts.append(session)

	# Returns a list of session counts
	return session_counts

#-----------------------------------------------------------------------------------------------

### GET PAGE VIEWS PER SESSIONS

def pages_per_session(sid):

	page_count = 0
	all_page_counts = []
	all_pages_per_session = []

	# Get page counts
	for val in sid:
		#print len(pageviews[val])
		for i in range(0, len(pageviews[val])):
			#print len(pageviews[val][i])
			page_count += len(pageviews[val][i])
		#print ""
		all_page_counts.append(page_count)
		session_count = len(pageviews[val])
		#print page_count
		pages_per_session = float(page_count)/float(session_count)
		all_pages_per_session.append(pages_per_session)
		page_count = 0
		

	#print all_page_counts
	return all_pages_per_session

#-----------------------------------------------------------------------------------------------

### MAIN

pageviews = {}

# This is the number of seconds in 30 minutes
session_time = 1800

# Stores the session counts for each SID in a new column.
df['Sessions'] = sessions(df['demandbase_sid'], df['date_time'], session_time)

# Stores the pages per session for each SID in a new column.
df['Pages / Session'] = pages_per_session(df['demandbase_sid'])

# Get the last row for each SID, this will have the max session and pages/session values
# and ensures there is only one row for each SID.
sessions_df = df.drop_duplicates(subset='demandbase_sid', keep='last')

# Write final dataframe to output file
f2 = 'test.xlsx'
writer = pd.ExcelWriter(f2, engine = 'xlsxwriter')
sessions_df.to_excel(writer, sheet_name = 'Sessions', index = False, columns = ['company_name', \
	'city', 'country', 'demandbase_sid', 'Sessions', 'Pages / Session'])

writer.save()

#-------------------------------------------------------------------------------------------------

# Print Sessions for a Test SID
print pageviews[58474121]
