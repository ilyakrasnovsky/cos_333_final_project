
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
from email.mime.text import MIMEText
import base64
from apiclient import errors

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-webapp.json
SCOPES = ['https://www.googleapis.com/auth/calendar',  
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/gmail.compose',
        'https://www.googleapis.com/auth/gmail.send']
#SCOPES = 'https://www.googleapis.com/auth/admin.directory.resource.calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python WebApp'

'''
def exchange_code(authorization_code):
  """Exchange an authorization code for OAuth 2.0 credentials.

  Args:
    authorization_code: Authorization code to exchange for OAuth 2.0
                        credentials.
  Returns:
    oauth2client.client.OAuth2Credentials instance.
  Raises:
    CodeExchangeException: an error occurred.
  """
  flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
  flow.redirect_uri = REDIRECT_URI
  try:
    credentials = flow.step2_exchange(authorization_code)
    return credentials
  except FlowExchangeError, error:
    logging.error('An error occurred: %s', error)
    raise CodeExchangeException(None)

def get_user_info(credentials):
  """Send a request to the UserInfo API to retrieve the user's information.

  Args:
    credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                 request.
  Returns:
    User information as a dict.
  """
  user_info_service = build(
      serviceName='oauth2', version='v2',
      http=credentials.authorize(httplib2.Http()))
  user_info = None
  try:
    user_info = user_info_service.userinfo().get().execute()
  except errors.HttpError, e:
    logging.error('An error occurred: %s', e)
  if user_info and user_info.get('id'):
    return user_info
  else:
    raise NoUserIdException()
'''
def get_authorization_url(email_address, state):
  """Retrieve the authorization URL.

  Args:
    email_address: User's e-mail address.
    state: State for the authorization URL.
  Returns:
    Authorization URL to redirect the user to.
  """
  flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
  flow.params['access_type'] = 'offline'
  flow.params['approval_prompt'] = 'force'
  flow.params['user_id'] = email_address
  flow.params['state'] = state
  return flow.step1_get_authorize_url(REDIRECT_URI)
'''
def get_credentials(authorization_code, state):
  """Retrieve credentials using the provided authorization code.

  This function exchanges the authorization code for an access token and queries
  the UserInfo API to retrieve the user's e-mail address.
  If a refresh token has been retrieved along with an access token, it is stored
  in the application database using the user's e-mail address as key.
  If no refresh token has been retrieved, the function checks in the application
  database for one and returns it if found or raises a NoRefreshTokenException
  with the authorization URL to redirect the user to.

  Args:
    authorization_code: Authorization code to use to retrieve an access token.
    state: State to set to the authorization URL in case of error.
  Returns:
    oauth2client.client.OAuth2Credentials instance containing an access and
    refresh token.
  Raises:
    CodeExchangeError: Could not exchange the authorization code.
    NoRefreshTokenException: No refresh token could be retrieved from the
                             available sources.
  """
  email_address = ''
  try:
    credentials = exchange_code(authorization_code)
    user_info = get_user_info(credentials)
    email_address = user_info.get('email')
    user_id = user_info.get('id')
    if credentials.refresh_token is not None:
      store_credentials(user_id, credentials)
      return credentials
    else:
      credentials = get_stored_credentials(user_id)
      if credentials and credentials.refresh_token is not None:
        return credentials
  except CodeExchangeException, error:
    logging.error('An error occurred during code exchange.')
    # Drive apps should try to retrieve the user and credentials for the current
    # session.
    # If none is available, redirect the user to the authorization URL.
    error.authorization_url = get_authorization_url(email_address, state)
    raise error
  except NoUserIdException:
    logging.error('No user ID could be retrieved.')
  # No refresh token has been retrieved.
  authorization_url = get_authorization_url(email_address, state)
  raise NoRefreshTokenException(authorization_url)
'''
def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-webapp.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, ' '.join(SCOPES))
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    #print 'Message Id: %s % message['id']'
    return message
  except errors.HttpError, error:
    print ("error")
   #print 'An error occurred: %s' % error

def main():
    """Shows basic usage of the Google Calendar API.
    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)


    print("--------------------------------")
    print("SENDING EMAIL MESSAGE")
    print("---------------------------------")
    m = "This is a test message to test messaging"
    message = CreateMessage("amalleo@princeton.edu", "amalleo@princeton.edu", "test message", m)
    SendMessage(service,"amalleo@princeton.edu",message)
    #MY CHANGES
    
    '''
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
    '''

if __name__ == '__main__':
    main()
