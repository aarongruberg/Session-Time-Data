# Get the number of sessions and page views per session where a session is the total page views 
# for a given SID over 30 minute period from first page view

import pandas as pd
import sys  
from datetime import datetime
import numpy as np

# Changed default string encoding from 'ascii' to 'utf8'
reload(sys)  
sys.setdefaultencoding('utf8')

### READ CSV 

f = 'ftse.0510-0622.2018.api.logs_SAMPLE.csv'

df = pd.read_csv(f, skiprows=None)
#df = df.head(500)

# Convert to datetime format
df['date_time'] =  pd.to_datetime(df['date_time'])
df['date_time'] = df['date_time'].values
#print type(df['date_time'])
#print df


#---------------------------------------------------------------------------------------------

### GET SESSIONS FOR EACH SID

# First find the time between two pageviews for a single SID
# Test SID: '9643371'
def sessions(sid, datetime, session_time):

	# SID is not in pageviews dictionary
	if sid not in pageviews.keys():
		
		pageviews[sid] = [[datetime]]

	
	# SID only has 1 list of time values, the last element is a numpy object.
	# Compare datetime to the first element.
	elif len(pageviews[sid]) == 1:

		initial_time = pageviews[sid][-1][0]

		diff = datetime - initial_time
		diff = diff.seconds

		if diff <= session_time:

			pageviews[sid][-1].append(datetime)

		else:

			pageviews[sid] = pageviews[sid]
			pageviews[sid].append([datetime])

	
	# SID time values are stored in a list of lists.
	# Compare datetime to the first element of the last list.
	else:

		initial_time = pageviews[sid][-1][0]

		diff = datetime - initial_time
		diff = diff.seconds

		if diff <= session_time:

			pageviews[sid][-1].append(datetime)

		else:

			pageviews[sid].append([datetime])

	session_count = len(pageviews[sid])

	return session_count

#-----------------------------------------------------------------------------------------------

### GET PAGE VIEWS PER SESSIONS

def pages_per_session(sid):

	print pageviews[sid]
	print " "

#-----------------------------------------------------------------------------------------------

### MAIN

pageviews = {}

# This is the number of seconds in 30 minutes
session_time = 1800

#print df['date_time'].values

df['sessions'] = df.apply(lambda x: sessions(x['demandbase_sid'], x['date_time'], session_time), axis=1)


pages_per_session(9262953)





