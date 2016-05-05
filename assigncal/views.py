'''
module : views

handles HTTP requets and renders views
'''

from __future__ import print_function
import httplib2
import os

#Django based dependencies
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings

#Non-Django based dependencies
import backend
import CASClient
import re
import os

# oauth2client
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
from apiclient import errors
import argparse

#Model data structures
from assigncal.models import Student, Course

# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

@ensure_csrf_cookie
def cal(request):
    if (request.session.get('netid') == None):
        raise Http404('')
    context = {"courses" : request.session.get('courses')}
    return render(request, 'assigncal/cal.html', context)

#Get the next date as a (year, month, day) tuple
#given the current date as the same tuple
def nextDate(year, month, day):
    if (month in [1,3,5,7,8,10,12]):
        if (day == 31):
            if (month == 12):
                return (year + 1, 1, 1)
            else:
                return (year, month + 1, 1)
        else:
            return (year, month, day + 1)
    elif (month in [4,6,9,11]):
        if (day == 30):
            return (year, month + 1, 1)
        else:
            return (year, month, day + 1)
    else:
        if (year % 4 == 0):
            if (day == 29):
                return (year, month + 1, 1)
            else:
                return (year, month, day + 1)
        else:
            if (day == 28):
                return (year, month + 1, 1)
            else:
                return (year, month, day + 1)

#Get the next 30 minute block as a (year, month, day, hour, minute) tuples
#from the current block as the same tuple
def nextClock(year, month, day, hour, minute):
    if (minute == 30):
        if (hour == 23):
            (year, month, day) = nextDate(year, month, day)
            return (year, month, day, 0, 0)
        else:
            return (year, month, day, hour + 1, 0)
    else:
        return (year, month, day, hour, 30)

#Generate free list from start
#time and end time, i.e., break
#it into 30 minutes blocks 
def makeFreeList(starttime, endtime):
    (startdate, startclock) = (starttime.split('T')[0],
                               starttime.split('T')[1]) 
    (enddate, endclock) = (endtime.split('T')[0],
                               endtime.split('T')[1]) 
    timedict = dict()
    if (starttime != endtime):
        (year, month, day) = (int(startdate.split('-')[0]),
                             int(startdate.split('-')[1]),
                             int(startdate.split('-')[2]))
        (YYYYe, MMe, DDe) = (int(enddate.split('-')[0]),
                             int(enddate.split('-')[1]),
                             int(enddate.split('-')[2]))
        (hour, minute) = (int(startclock.split(':')[0]),
                          int(startclock.split(':')[1]))
        (HHe, mme) = (int(endclock.split(':')[0]),
                          int(endclock.split(':')[1]))
        while (year < YYYYe):
            time = "%04d-%02d-%02dT%02d:%02d:00" % \
                    (year, month, day, hour, minute)
            timedict[time] = ""
            (year, month, day, hour, minute) = nextClock(year, month, day, hour, minute)
        while (month < MMe):
            time ="%04d-%02d-%02dT%02d:%02d:00" % \
                    (year, month, day, hour, minute)
            timedict[time] = ""
            (year, month, day, hour, minute) = nextClock(year, month, day, hour, minute)
        while (day < DDe):
            time ="%04d-%02d-%02dT%02d:%02d:00" % \
                    (year, month, day, hour, minute)
            timedict[time] = ""
            (year, month, day, hour, minute) = nextClock(year, month, day, hour, minute)
        while (hour < HHe):
            time ="%04d-%02d-%02dT%02d:%02d:00" % \
                    (year, month, day, hour, minute)
            timedict[time] = ""
            (year, month, day, hour, minute) = nextClock(year, month, day, hour, minute)
        while (minute < mme):
            time ="%04d-%02d-%02dT%02d:%02d:00" % \
                    (year, month, day, hour, minute)
            timedict[time] = ""
            (year, month, day, hour, minute) = nextClock(year, month, day, hour, minute)
        timedict[endtime] = ""
    return timedict

#save free time blocks to users freelist
@ensure_csrf_cookie
def save(request):
    if (request.method == "POST"):
        Sdict = {"freedict" : makeFreeList(request.POST.dict()['starttime'],
                              request.POST.dict()['endtime'])
                }
        backend.addTimesToStudent(request.session.get('netid'), Sdict)
        #context = {"courses" : request.session.get('courses')}
        #return render(request, 'assigncal/cal.html', context)
        return HttpResponse("OK")
    else:
        raise Http404('')

#remove free time blocks from users freelist
@ensure_csrf_cookie
def remove(request):
    if (request.method == 'POST'):
        toRemove = makeFreeList(request.POST.dict()['starttime'],
                              request.POST.dict()['endtime'])
        Sdict = backend.getStudent(request.session.get('netid'))
        if (Sdict.has_key('freedict')):
            freedict = Sdict['freedict']
            for i in toRemove.keys():
                freedict.pop(i, None)
            backend.forceUpdateStudent(request.session.get('netid'), {"freedict" : freedict})
        #context = {"courses" : request.session.get('courses')}
        #return render(request, 'assigncal/cal.html', context)
        return HttpResponse("OK")
    else:
        raise Http404('')

#Makes a list of events from dict of starttimes and endtimes
#for a studen,t namely, from a netid
def makeEventsFromNetid(netid):
    events = []
    Sdict = backend.getStudent(netid)
    if (Sdict.has_key('freedict')):
        freedict = Sdict['freedict']
        useddates = []
        for free in freedict.keys():
            (date, clock) = (free.split('T')[0],
                            free.split('T')[1])
            (year, month, day) = (int(date.split('-')[0]),
                             int(date.split('-')[1]),
                             int(date.split('-')[2]))
            (hour, minute) = (int(clock.split(':')[0]),
                              int(clock.split(':')[1]))                
            (year, month, day, hour, minute) = nextClock(year, month, day, hour, minute)
            nextfree = "%04d-%02d-%02dT%02d:%02d:00" % \
                    (year, month, day, hour, minute)
            if (date not in useddates):
                events.append({
                        "title" : netid + " is free!",
                        "start" : date,
                        "color" : "white",
                    })
                events.append({
                        "title" : netid + " is free!",
                        "start" : date,
                        "color" : "white",
                        "rendering" : "background"
                    })
                useddates.append(date)
            events.append({
                    "title" : netid,
                    "start" : free,
                    "end" : nextfree,
                    "color" : "white",
                    "rendering" : "background"
                })
    return events

#Makes a list of events from dict of starttimes and endtimes
#for a course, namely, from a course name
def makeEventsFromCourse(coursename):
    events = []
    Cdict = backend.getCourse(coursename)
    globalFrees = dict()
    #Assemble global dictionary of free times and frequencies
    #of students in those free time
    for i in Cdict['students']:
        student = backend.getStudent(i)
        if (student.has_key('freedict')):
            freedict = student['freedict']
            for free in freedict.keys():
                if (globalFrees.has_key(free)):
                    globalFrees[free].append(student['netid']) #= globalFrees[free] + 1
                else:
                    globalFrees[free] = [student['netid']] #1
    #Translate the globalFrees dictionary into a list of events
    useddates = []
    for free in globalFrees.keys():
        (date, clock) = (free.split('T')[0],
                    free.split('T')[1])
        (year, month, day) = (int(date.split('-')[0]),
                         int(date.split('-')[1]),
                         int(date.split('-')[2]))
        (hour, minute) = (int(clock.split(':')[0]),
                          int(clock.split(':')[1]))                
        (year, month, day, hour, minute) = nextClock(year, month, day, hour, minute)
        nextfree = "%04d-%02d-%02dT%02d:%02d:00" % \
                (year, month, day, hour, minute)
        if (date not in useddates):
            events.append({
                    "title" : str(len(globalFrees[free])) + " people",
                    "start" : date,
                    "color" : colorCode(len(globalFrees[free])),
                })
            events.append({
                    "title" : str(len(globalFrees[free])) + " people",
                    "start" : date,
                    "color" : colorCode(len(globalFrees[free])),
                    "rendering" : "background"
                })
            #get names in the list for "See Names"
            if (len(globalFrees[free]) <= 1):
                events.append({
                        "title": str(len(globalFrees[free])) + " people",
                        "start": date,
                        "color" : colorCode(len(globalFrees[free]))
                        #"id" : 9999
                })
            for netid in globalFrees[free]:
                events.append({
                        "title" : netid,
                        "start" : date,
                        "textcolor" : "white",
                        "color" : colorCode(len(globalFrees[free]))
                    })
            useddates.append(date)
        events.append({
                "title" : "lol",
                "start" : free,
                "end" : nextfree,
                "color" : colorCode(len(globalFrees[free])),
                "rendering" : "background"
            })
    return events

#Return color code for free time event based on number of 
#students for that time 
def colorCode(numStudents):
    color = "white"
    if (numStudents <= 1):
        color = "red"
    elif (numStudents == 2):
        color = "orange"
    elif (numStudents == 3):
        color = "yellow"
    elif (numStudents == 4):
        color = "green"
    else:
        color = "#568203"
    return color

#adds current course selection from tab as a session variable,
#returns ok response, so that client side can refetch events
#via GET request to eventfeed
@ensure_csrf_cookie
def courses(request):
    if (request.method == "POST"):
        request.session['course'] = request.POST.dict()['course']
        #context = {"courses" : request.session.get('courses')}
        return HttpResponse("OK")
    else:
        raise Http404('')

# set session variable for email, return OK response
def email(request):
    if (request.method == "POST"):
        request.session['email'] = request.POST.dict()['email']
        print(request.session.get('email'))
        return HttpResponse("OK")
    elif (request.method == "GET"):
        emailvar = {'email': request.session.get('email')}
        return JsonResponse(emailvar)
    else:
        raise Http404('')


#fetches events from either user or course based on session
#variable from firebase, gives JSON response of the events
#to client side
def eventfeed(request):
    print ("in eventfeed and session course is " + str(request.session.get('course')))
    if (request.session.get('course') == "myFrees"):
        events = makeEventsFromNetid(request.session.get('netid'))
    else:
        events = makeEventsFromCourse(request.session.get('course'))
    context = {"events" : events}
    return JsonResponse(context)

def login(request):
    #Set SITE_URL from Django settings file to
    #session variable for the first time
    request.session['SITE_URL'] = settings.SITE_URL

    #Redirect to CAS login, will append ticket in response
    SITE_URL = request.session.get('SITE_URL')
    print (SITE_URL)
    C = CASClient.CASClient(SITE_URL)
    login_url = C.Authenticate()
    
    return HttpResponseRedirect(login_url)

def gotoBB(request):
    #Get SITE URL from Django session
    request.session['SITE_URL'] = settings.SITE_URL
    SITE_URL = request.session.get('SITE_URL')
    
    #Get ticket
    if (request.GET.dict().has_key('ticket') == False):
        raise Http404('')
    ticket = request.GET.dict()['ticket']    
    
    #Validate ticket, get netid from it
    C = CASClient.CASClient(SITE_URL)
    netid = C.Validate(ticket)

    #sSave netid to Django session for use in other views
    request.session['netid'] = netid

    #Make Student object out of netid    
    Sobject = Student(netid)
    
    #Add dictified Student object to firebase
    backend.addStudent(Sobject.dictify())

    driver = webdriver.Chrome()
    driver.get("https://blackboard.princeton.edu")
    driver.find_element_by_xpath("//div[@title='I have a valid Princeton NetID and Password']").click()
    user = driver.find_element_by_id("username")
    passw = driver.find_element_by_id("password")
    user.send_keys(netid)
    curr_url = driver.current_url
    #passw.send_keys(raw_input("Enter something"))
    #passw.send_keys(getpass.getpass())

    #time.sleep(10)
    #WebDriverWait(driver,100).until(curr_url != driver.current_url)
    # wait until user gets past login page
    # try:
    #     WebDriverWait(driver, 120).until(lambda driver: driver.find_element_by_id("globalNavPageNavArea"))
    # finally:
    #     driver.close()
        # return back to login page?
    WebDriverWait(driver, 120).until(lambda driver: driver.find_element_by_id("globalNavPageNavArea"))

    #driver.find_element_by_xpath("//input[@value='Login']").click()
    regexp1 = re.compile("Spring 2016.*?</div>", flags=re.DOTALL)
    coursecontent = regexp1.search(driver.page_source).group(0)
    regexp2 = re.compile(">.*?_S2016.*?<")
    courses = re.findall(regexp2,coursecontent)
    regexp3 = re.compile("\">.*?<")
    courselist = []
    course_list = {}
    # scrape courses
    for course in courses:
        c = regexp3.search(course)
        if (c != None):
            courselist.append(c.group(0))

    for course in courselist:
        course = course.split('>')[1]
        course = course.split('<')[0]
        regex = course[:6]
        regex = regex.replace('-', '_')
        if (len(regex) == 6):
            course_list[regex] = regex
        #regex = re.findall(".*?_",course)[0]
        #print(regex)

    # scrape assignments
    #regexp4 = re.compile("\"/webapps.*?\"")
    regexp4 = re.compile("<a.*?</a>", flags=re.DOTALL)
    ass_link = re.findall(regexp4,coursecontent)
    # goes through each course's assignment page
    for i in ass_link:
        re_url = re.findall("/webapps.*?top", i)[0]
        url_val = re_url.replace("amp;", "")
        url = "https://blackboard.princeton.edu" + url_val
        driver.get(url)

        # click on "Assignments"
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_link_text("Assignments")).click()
        # driver.find_element_by_link_text("Assignments").click()

        # find assignments
        regexp1 = re.compile("contentListItem.*?</div>", flags=re.DOTALL)
        listitems = re.findall(regexp1, driver.page_source)

        assignmentlinks = []
        for items in listitems:
            link = regexp2.search(items)
            if (link != None):
                assignmentlinks.append(link.group(0))

        # filter out links, exclude solutions
        regexp4 = re.compile("href=.*?>", flags=re.DOTALL)
        regexp3 = re.compile(">.*?</span>", flags=re.DOTALL)
        assignment_list = {}

        for a in assignmentlinks:
            name = regexp3.search(a)
            link = regexp4.search(a)
            if (name != None):
                name = (name.group(0)).split('>')[2]
                name = name.split('<')[0]
            if (link != None):
                link = (link.group(0)).split('"')[1]
                link = link.split('"')[0]
            url = "www.blackboard.princeton.edu" + link
            assignment_list[name] = url
            

    driver.close()

    #Automated scraping and browsing of blackboard called here
    #After scraping
    # courses = { "COS 424" : "COS424",
    #             "EGR 333" : "COS333",
    #             "MAE 426" : "MAE426",
    #             "CLA 255" : "CLA255",
    #             "COS 217" : "COS217"}

    #request.session['courses'] = course_list
    print(course_list)
    request.session['courses'] = course_list
    request.session['course'] = 'myFrees'
    #iterate over newly scraped courses
    for i in request.session.get('courses').values():
        #if not in db, add it to db
        newCourse = Course(i,[request.session.get('netid')],"2016-01-13T12:30:00", assignment_list)
        added = backend.addCourse(newCourse.dictify())
        #if in db, add student's netid to course
        if (added == False):
            existCourse = backend.getCourse(i)
            if (request.session.get('netid') not in existCourse['students']):
                existCourse['students'].append(request.session.get('netid'))
                backend.updateCourse(i, existCourse)
    return HttpResponseRedirect("/cal")


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
    flags = None
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, ' '.join(SCOPES))
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run_flow(flow, store)
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
                {'email': 'ghong@princeton.edu'},
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

    freeStudents = []
    for i in fetchFreeStudents(request, request.POST.dict()['starttime'], request.POST.dict()['endtime']):
        free = {}
        free['email'] = i
        freeStudents.append(free)
    print(freeStudents)

    new_event = {
        'summary': request.session.get('course') + ' Problem Set Session',
        'location': 'Princeton University, Princeton, NJ, 08544',
        'description': 'Let\'s collaborate on this PSET!',
        'start': {
            # 'dateTime': '2016-07-07T09:00:00-00:00',
            'dateTime': request.POST.dict()['starttime'],
            'timeZone': 'America/New_York',
          },
        'end': {
            'dateTime': request.POST.dict()['endtime'],
            # 'dateTime': '2016-07-07T17:00:00-05:00',
            'timeZone': 'America/New_York',
          },
          #'recurrence': [
          #  'RRULE:FREQ=DAILY;COUNT=2'
          #],
          #'attendees': freeStudents,
          'attendees': [{'email': 'striketheghong@gmail.com'}],
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
            print(calid)
            break
    
    #Use the extracted id to get the calender object via the get() request
    if (calid != None):
        #Add new event request
        print("INHERE")
        add_event_req = service.events().insert(calendarId=calid, body=new_event, sendNotifications=True)
        add_event_req.execute()
    else:
        print ("Calendar with name : " + calname + " not found!")


    return HttpResponseRedirect("/cal")

# find free students
def fetchFreeStudents(request, starttime, endtime):
    course = request.session.get('course')
    allStudents = backend.getCourse(course)['students']
    availableStudents = []
    for i in allStudents:
        if backend.getStudent(i).has_key('freedict'):
            if backend.getStudent(i)['freedict'].has_key(starttime):
                availableStudents.append(str(i) + "@princeton.edu")
    print(availableStudents)

    return availableStudents
        


