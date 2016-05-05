

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-webapp.json
SCOPES = ['https://www.googleapis.com/auth/calendar',  
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/gmail.compose',
        'https://www.googleapis.com/auth/gmail.send']
#SCOPES = 'https://www.googleapis.com/auth/admin.directory.resource.calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python WebApp'

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


def add_event(calname,title,location, descr, start, end):
    event = None
    calendar = get_calendar(calname)
    if (calendar != None):
        new_event = {
              'summary': title,
              'location': location,
              'description': descr,
              'start': {
                'dateTime': start,
                'timeZone': 'America/New_York',
              },
              'end': {
                'dateTime': end,
                'timeZone': 'America/New_York',
              },
              #'recurrence': [
              #  'RRULE:FREQ=DAILY;COUNT=2'
              #],
              'attendees': [
                {'email': 'amalleo@princeton.edu'},
              ],
              'reminders': {
                'useDefault': False,
                'overrides': [
                  {'method': 'email', 'minutes': 24 * 60},
                  {'method': 'popup', 'minutes': 10},
                ],
              },
            }
        add_event_req = service.events().insert(sendNotifications=True, calendarId=calendar['id'], body=new_event)
        event = add_event_req.execute()
    return event


def sendemail(request):

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)


    #HTTP request for a list of the user's calendars
    usr_cals_req = service.calendarList().list()
    
    #Execute the request, returns data in an object we call usr_cals
    usr_cals = usr_cals_req.execute()

    createnew = True
    #If user does not already have assignment calendar we make one:
    for i in usr_cals['items']:
       if i['summary'] == 'AssignCal':
            createnew = False
            calid = i['id']

    if createnew:
        new_cal = {
        "kind": "calendar#calendar", # Type of the resource ("calendar#calendar").
        "description": "This is the calendar to keep track of study session times", # Description of the calendar. Optional.
        "summary": "AssignCal", # Title of the calendar.
        #"etag": "A String", # ETag of the resource.
        "timeZone": "America/New_York", # The time zone of the calendar. (Formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich".) Optional.
         # Identifier of the calendar. To retrieve IDs call the calendarList.list() method.
            }
        new_cal_req = service.calendars().insert(body=new_cal)
        new_created_cal = new_cal_req.execute()

    new_event = {
        'summary': 'COS 333 TEST EVENT',
        'location': 'Princeton University, Princeton, NJ, 08544',
        'description': 'Let\'s collaborate on this PSET!',
        'start': {
            'dateTime': '2016-07-07T09:00:00-00:00',
            'timeZone': 'America/New_York',
          },
        'end': {
            'dateTime': '2016-07-07T17:00:00-05:00',
            'timeZone': 'America/New_York',
          },
          #'recurrence': [
          #  'RRULE:FREQ=DAILY;COUNT=2'
          #],
          'attendees': [
            {'email': 'amalleo@princeton.edu'},
            {'email': 'akmalleo3@gmail.com'}
          ],
        #'reminders': {
        #    'useDefault': False,
        #    'overrides': [
        #      {'method': 'email', 'minutes': 24 * 60},
        #      {'method': 'email', 'minutes': 10},
         #   ],
         # },
        }

    #Extract a particular calendar id by name
    calid = None
    calname = 'AssignCal'

    for i in usr_cals['items']:
        if (i['summary'] == calname):
            calid = i['id']
            break
    
    #Use the extracted id to get the calender object via the get() request
    if (calid != None):
        #Add new event request
        add_event_req = service.events().insert(calendarId=calid, body=new_event, sendNotifications=True)
        add_event_req.execute()
    else:
        print ("Calendar with name : " + calname + " not found!")

