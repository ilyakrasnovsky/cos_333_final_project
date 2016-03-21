'''
module : Google Calendar API Utilities

provides classes/functions helpful for managing our Google
calendars via their API

'''
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-webapp.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'COS 333 Assignment Calendars'

'''
function : get_credentials()

-Gets valid user credentials from storage.

-If nothing has been stored, or if the stored credentials are invalid,
the OAuth2 flow is completed to obtain the new credentials.

Returns:
    Credentials, the obtained credential.
'''
def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-webapp.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials






'''
function main()

tester client that shows basic usage of the Google Calendar API.

Creates a Google Calendar API service object and outputs a list of the next
10 events on the user's calendar.

'''
def main():
    #Creates a Google Calendar API service object from our
    #credentials
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    #MY CHANGES
    
    print ("--------------------------------")
    print ("NAMES OF ALL THE USER'S CALENDARS")
    print ("--------------------------------")
    #HTTP request for a list of the user's calendars
    usr_cals_req = service.calendarList().list()
    
    #Execute the request, returns data in an object we call usr_cals
    usr_cals = usr_cals_req.execute()    
    
    #Iterate over the "items" field of usr_cals and print the "summary"
    #field of each item, which corresponds to printing the name of each
    #calendar
    for i in usr_cals['items']:
        print (i['summary'])
    
    print ("--------------------------------")
    print ("FINDING/FETCHING A USER'S CALENDAR BY NAME/ID")
    print ("--------------------------------")
    #Extract a particular calendar id by name
    calid = None
    calname = 'new calendar'
    for i in usr_cals['items']:
        if (i['summary'] == calname):
            calid = i['id']
            break

    #Use the extracted id to get the calender object via the get() request
    if (calid != None):
        cal_byid_req = service.calendarList().get(calendarId=calid)
        cal_byid = cal_byid_req.execute()
        print ("Found " + cal_byid['summary'] + " by id.")
        print ("The time zone of " + cal_byid['summary'] + " is " + cal_byid['timeZone'])
    else:
        print ("Calendar with name : " + calname + " not found!")

    
    #Programtically create a new calendar using the insert() from calendars() request
    print ("--------------------------------")
    print ("GENERATING A NEW CALENDAR AND VERIFYING ITS NAME AND ID")
    print ("--------------------------------")
    #princeton_orange = "#FF8F00"
    new_cal = {
    "kind": "calendar#calendar", # Type of the resource ("calendar#calendar").
    "description": "This is a test of Programtically creating a new calendar", # Description of the calendar. Optional.
    "summary": "A new calendar", # Title of the calendar.
    #"etag": "A String", # ETag of the resource.
    "location": "Princeton, NJ, USA", # Geographic location of the calendar as free-form text. Optional.
    "timeZone": "America/New_York", # The time zone of the calendar. (Formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich".) Optional.
    #"id": "A String", # Identifier of the calendar. To retrieve IDs call the calendarList.list() method.
            }

    #FORMAT MUST BE A DICT, NOT JSON, AND THEREFORE NO COMMENTS
    new_cal_req = service.calendars().insert(body=new_cal)
    new_created_cal = new_cal_req.execute()
    
    print ("Name of new calendar is " + new_created_cal['summary'])
    print ("calendarId of new calendar is " + new_created_cal['id'])

    print ("--------------------------------")
    print ("DELETING THE JUST CREATED CALENDAR AND VERIFYING THAT IT IS GONE")
    print ("--------------------------------")
    
    del_cal_req = service.calendars().delete(calendarId=new_created_cal['id'])
    del_cal_req.execute()

    #HTTP request for a list of the user's calendars
    usr_cals_req = service.calendarList().list()
    
    #Execute the request, returns data in an object we call usr_cals
    usr_cals = usr_cals_req.execute()    
    
    #Extract a particular calendar id by name
    calid = None
    calname = 'A new calendar'
    for i in usr_cals['items']:
        if (i['summary'] == calname):
            calid = i['id']
            break

    #Use the extracted id to get the calender object via the get() request
    if (calid != None):
        cal_byid_req = service.calendarList().get(calendarId=calid)
        cal_byid = cal_byid_req.execute()
        print ("Found " + cal_byid['summary'] + " by id.")
        print ("The time zone of " + cal_byid['summary'] + " is " + cal_byid['timeZone'])
    else:
        print ("Calendar with name : " + calname + " not found!")


    print ("--------------------------------")
    print ("ADDING A NEW EVENT TO AN EXISTING CALENDAR")
    print ("--------------------------------")

    new_event = {
          'summary': 'COS 333 TEST EVENT',
          'location': 'Princeton University, Princeton, NJ, 08544',
          'description': 'Let\'s not fail cos 333 lol',
          'start': {
            'dateTime': '2016-03-20T09:00:00-05:00',
            'timeZone': 'America/New_York',
          },
          'end': {
            'dateTime': '2016-03-20T17:00:00-05:00',
            'timeZone': 'America/New_York',
          },
          #'recurrence': [
          #  'RRULE:FREQ=DAILY;COUNT=2'
          #],
          #'attendees': [
          #  {'email': 'lpage@example.com'},
          #  {'email': 'sbrin@example.com'},
          #],
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'email', 'minutes': 24 * 60},
              {'method': 'email', 'minutes': 10},
            ],
          },
        }

    #Extract a particular calendar id by name
    calid = None
    calname = 'new calendar'
    for i in usr_cals['items']:
        if (i['summary'] == calname):
            calid = i['id']
            print (calid)
            print(i['accessRole'])
            break

    #Use the extracted id to get the calender object via the get() request
    if (calid != None):
        #Add new event request
        add_event_req = service.events().insert(calendarId=calid, body=new_event)
        add_event_req.execute()
    else:
        print ("Calendar with name : " + calname + " not found!")

    #MY CHANGES

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        #print (event)
        #print(start, event['summary'])


if __name__ == '__main__':
    main()
