'''
module : views

handles HTTP requets and renders views
'''

#Django based dependencies
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings

#Non-Django based dependencies
import backend
import CASClient
import re
import mechanize
import requests
import urllib2

#Model data structures
from assigncal.models import Student, Course

#from django.core.servers import basehttp

#del basehttp._hop_headers['Transfer-Encoding']
#del basehttp._hop_headers['proxy-authorization']

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
    if (request.method == 'POST'):
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
def makeEvents(netid):
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
    '''
    prevstart = events[0]['start']
    for i in range(0, len(events)):
        if (i >= 1):
            if (events[i]['start'] == events[i-1]['start']):
                print ("same time found")
                pass
            else:
                print (events[i]['start'])
                pass
    '''
    return events

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

#fetches events from either user or course based on session
#variable from firebase, gives JSON response of the events
#to client side
def eventfeed(request):
    #print ("in eventfeed and session course is " + str(request.session.get('course')))
    if (request.session.get('course') == "myFrees"):
        events = makeEvents(request.session.get('netid'))
        context = {'events' : events}
    else:
        context = {'events' : [
                        {
                            "title": '4 people',
                            "rendering": 'background',
                            "start": '2016-01-12',
                            "color" : '#568203'
                        },
                        {
                            "title": '4 people',
                            "start": '2016-01-12',
                            "color" : '#568203',
                            "id" : 1
                        },
                        {
                            "title": "DjangoAlex",
                            "start": '2016-01-12',
                            "textColor" : "white",
                            "color" : 'black'
                        },
                        {
                            "title": 'Betty',
                            "start": '2016-01-12',
                            "textColor" : "white",
                            "color" : 'black'
                        },
                        {
                            "title": 'Chloe',
                            "start": '2016-01-12',
                            "textColor" : "white",
                            "color" : 'black'
                        },
                        {
                            "title": 'Mark',
                            "start": '2016-01-12',
                            "textColor" : "white",
                            "color" : 'black'
                        },
                        {
                            "title": 'Block1',
                            "rendering": 'background',
                            "start": '2016-01-12T10:30:00',
                            "end": '2016-01-12T11:00:00',
                            "color" : 'red',
                            "id" : 2
                        },
                        {
                            "title": 'Block2',
                            "rendering": 'background',
                            "color" : 'orange',
                            "start": '2016-01-12T11:00:00',
                            "end": '2016-01-12T11:30:00',
                            "id" : 3
                        },
                        {
                            "title": 'Block3',
                            "rendering": 'background',
                            "color" : 'yellow',
                            "start": '2016-01-12T11:30:00',
                            "end": '2016-01-12T12:00:00',
                            "id" : 4
                        },
                        {
                            "title": 'Block4',
                            "rendering": 'background',
                            "start": '2016-01-12T12:00:00',
                            "color" : 'light green',
                            "end" : '2016-01-12T12:30:00',
                            "id" : 5
                        },
                        {
                            "title": 'Block5',
                            "rendering": 'background',
                            "start": '2016-01-12T12:30:00',
                            "color" : 'green',
                            "end" : '2016-01-12T13:00:00',
                            "id" : 6
                        },
                        {
                            "title": '2 people',
                            "rendering": 'background',
                            "start": '2016-01-13',
                            "color" : 'orange'
                        },
                        {
                            "title": '2 people',
                            "start": '2016-01-13',
                            "color" : 'orange',
                            "id" : 1
                        },
                        {
                            "title": 'Alex',
                            "start": '2016-01-13',
                            "textColor" : "white",
                            "color" : 'black'
                        },

                        {
                            "title": 'Betty',
                            "start": '2016-01-13',
                            "textColor" : "white",
                            "color" : 'black'
                        },
                        {
                            "title": 'Block1',
                            "rendering": 'background',
                            "start": '2016-01-13T10:30:00',
                            "end": '2016-01-13T11:00:00',
                            "color" : 'red',
                            "id" : 2
                        },
                        {
                            "title": 'Block2',
                            "rendering": 'background',
                            "color" : 'orange',
                            "start": '2016-01-13T11:00:00',
                            "end": '2016-01-13T11:30:00',
                            "id" : 3
                        },
                        {
                            "title": 'Block3',
                            "rendering": 'background',
                            "color" : 'yellow',
                            "start": '2016-01-13T11:30:00',
                            "end": '2016-01-13T12:00:00',
                            "id" : 4
                        },
                        {
                            "title": 'Block4',
                            "rendering": 'background',
                            "start": '2016-01-13T12:00:00',
                            "color" : '#568203',
                            "end" : '2016-01-13T12:30:00',
                            "id" : 5
                        },
                        {
                            "title": 'Block5',
                            "rendering": 'background',
                            "start": '2016-01-13T12:30:00',
                            "color" : 'green',
                            "end" : '2016-01-13T13:00:00',
                            "id" : 6
                        },
                        {
                            "title": '3 people',
                            "rendering": 'background',
                            "start": '2016-01-14',
                            "color" : 'yellow'
                        },
                        {
                            "title": '3 people',
                            "start": '2016-01-14',
                            "color" : 'yellow',
                            "id" : 1
                        },
                        {
                            "title": 'Alex',
                            "start": '2016-01-14',
                            "textColor" : "white",
                            "color" : 'black'
                        },
                        {
                            "title": 'Betty',
                            "start": '2016-01-14',
                            "textColor" : "white",
                            "color" : 'black'
                        },
                        {
                            "title": 'Chloe',
                            "start": '2016-01-14',
                            "textColor" : "white",
                            "color" : 'black'
                        },
                        {
                            "title": 'Assignment due',
                            "rendering" : "background",
                            "start" : '2016-01-16',
                            "color" : 'white'
                        },
                        {
                            "title": 'Assignment 1 due',
                            "start" : '2016-01-16',
                            "textColor" : "black",
                            "color" : 'white',
                            "id" : 1
                        },
                        {
                            "title": '1 people',
                            "start" : '2016-01-16',
                            "textColor" : "black",
                            "color" : 'white',
                            "id" : 9999
                        },
                        {
                            "title": 'Chloe',
                            "start": '2016-01-16',
                            "textColor" : "white",
                            "color" : 'black'
                        },
                        {
                            "title": '1 people',
                            "rendering": 'background',
                            "start": '2016-01-15',
                            "color" : 'red'
                        },
                        {
                            "title": '1 people',
                            "start": '2016-01-15',
                            "color" : 'red',
                            "id" : 1
                        },
                        {
                            "title": '',
                            "start": '2016-01-15',
                            "color" : 'red',
                            "id" : 9999
                        },
                        {
                            "title": 'Alex',
                            "start": '2016-01-15',
                            "textColor" : "white",
                            "color" : 'black'
                        }
                ]
        }
    return JsonResponse(context)

def login(request):
    #Set SITE_URL from Django settings file to
    #session variable for the first time
    request.session['SITE_URL'] = settings.SITE_URL

    #Redirect to CAS login, will append ticket in response
    SITE_URL = request.session.get('SITE_URL')
    C = CASClient.CASClient(SITE_URL)
    login_url = C.Authenticate()
    
    br = mechanize.Browser()
    cookiejar = mechanize.LWPCookieJar() 
    br.set_cookiejar( cookiejar ) 
    print ("COOKIEJAR BEFORE GOING TO LOGIN_URL "),
    print(cookiejar)

    # Browser options 
    br.set_handle_equiv( True ) 
    br.set_handle_gzip( True ) 
    br.set_handle_redirect( True ) 
    br.set_handle_referer( True ) 
    br.set_handle_robots( False ) 
    br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 )
    br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ] 
    
    br.open(login_url) 
    request.session['cookiejar'] = cookiejar
    #print ("COOKIEJAR AFTER GOING TO LOGIN_URL "),
    #print(cookiejar)
    
    #req = mechanize.Request(login_url)
    #print ("req : " + str(req))
    #res = mechanize.urlopen(req)
    #print ("res : " + str(res))
    #print ("res.geturl : " + str(res.geturl()))
    #print ("res.info() : " + str(res.info()))
    
    #print ("res.read() : " + str(res.read()))

    '''
    request = urllib2.Request(login_url)
    response = urllib2.urlopen(request)
    r = HttpResponse(response.read())
    print(response.info().keys())

    for header in response.info().keys():
        if (header != "Transfer-Encoding"):
            r[header] = response.info()[header]
    '''
    
    '''
    res1 = requests.get(login_url)
    #res2 = requests.get(login_url)
    #print ("res1 :" + str(res1.text))
    print ("res1 : " + str(res1.cookies))
    #print ("res2 : " + str(res2.cookies))

    res_out = HttpResponse(res1.text)
    for header in res1.headers.keys():
        if (header != "Transfer-Encoding"):
            res_out[header] = res1.headers[header]
    '''

    #return r
    #return res_out
    #print (login_url)
    #print br.response()
    return HttpResponseRedirect(login_url)

def gotoBB(request):
    #Get SITE URL from Django session
    SITE_URL = request.session.get('SITE_URL')
    #print(SITE_URL)
    
    #full request url
    requrl = request.get_full_path()
    print ("http://localhost:8000" + requrl)

    #Get ticket
    if (request.GET.dict().has_key('ticket') == False):
        raise Http404('')
    ticket = request.GET.dict()['ticket']    
    print ("TICKET IS " + ticket)
    
    print ("REQUEST HOST IS :" + str(request.get_host()))

    #Validate ticket, get netid from it
    C = CASClient.CASClient(SITE_URL)
    (netid, br, cookiejar) = C.Validate(ticket)

    '''
    ck = mechanize.Cookie(version=0, name='CASTGC', value=ticket, port=None, port_specified=False, domain='authenticate.princeton.edu/cas', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
    cookiejar.set_cookie(ck)

    print("PRINTING cookiejar in gotoBB view as  :" + str(cookiejar))
    print
    br.open("https://blackboard.princeton.edu/webapps/bb-auth-provider-cas-bb_bb60/execute/casLogin?cmd=login&authProviderId=_142_1&redirectUrl=https://blackboard.princeton.edu/webapps/portal/execute/defaultTab")
    print ("COOKIEJAR AFTER GOING BACK TO CAS "),
    print(cookiejar)
    print

    BBhtml = br.response().read()
    with open("lol.html", "w") as lol:
        lol.write(BBhtml)
    '''
    
    #Requests library attempt to get cookies
    #sess = requests.Session()
    #print ("before sess.get")
    #sess_response = sess.get(requrl)
    #sess_response = requests.get("http://localhost:8000")
    #print ("after sess.get")
    #print (sess_response.cookies)
    #for i in sess_response.history:
    #    print (i)
        #print (i.cookies)    
    #print (sess.cookies.get_dict())    
    
    #print ("http://localhost:8000" + requrl)
    
    #Django session cookies
    #print (request.GET.dict())
    #sessionid = request.COOKIES['sessionid']
    #print ("COOKIES ARE " + str(request.COOKIES))
    #for i in request.META.keys():
    #    print (i + " "),
    #    print (request.META[i])

    #sSave netid to Django session for use in other views
    request.session['netid'] = netid

    #Make Student object out of netid    
    Sobject = Student(netid)
    
    #Add dictified Student object to firebase
    backend.addStudent(Sobject.dictify())
    
    #scrape(ticket)

    #Automated scraping and browsing of blackboard called here
    #After scraping
    courses = { "MAE 342" : "MAE342",
                "COS 333" : "COS333",
                "MAE 426" : "MAE426",
                "CLA 255" : "CLA255",
                "COS 217" : "COS217"}
    request.session['courses'] = courses
    request.session['course'] = None
    #Gina
    #return HttpResponseRedirect("https://blackboard.princeton.edu/webapps/bb-auth-provider-cas-bb_bb60/execute/casLogin?cmd=login&authProviderId=_142_1&redirectUrl=https://blackboard.princeton.edu/webapps/portal/execute/defaultTab")
    
    #return HttpResponseRedirect('https://blackboard.princeton.edu/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_121_1')

    #Regular
    return HttpResponseRedirect("/cal")

def scrape(ticket):
    #Mechanize library attempt to get cookies
    br = mechanize.Browser()
    cookiejar = mechanize.LWPCookieJar()
    br.set_cookiejar( cookiejar ) 
    print ("COOKIEJAR BEFORE GOING TO SITE_URL "),
    print(cookiejar)
    print
    ck = mechanize.Cookie(version=0, name='CASTGC', value=ticket, port=None, port_specified=False, domain='authenticate.princeton.edu/cas', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
    cookiejar.set_cookie(ck)

    print ("COOKIEJAR AFTER GOING TO SITE_URL AND ADDING TICKET"),
    print(cookiejar)    
    print
    # Browser options 
    br.set_handle_equiv( True ) 
    br.set_handle_gzip( True ) 
    br.set_handle_redirect( True ) 
    br.set_handle_referer( True ) 
    br.set_handle_robots( False ) 
    br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 )
    br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ] 
    br.open('http://localhost:8000')

    print ("COOKIEJAR AFTER GOING TO SITE_URL AND ADDING TICKET"),
    print(cookiejar)    
    print

    #br.open('https://authenticate.princeton.edu/cas/login')
    br.open("https://blackboard.princeton.edu/webapps/bb-auth-provider-cas-bb_bb60/execute/casLogin?cmd=login&authProviderId=_142_1&redirectUrl=https://blackboard.princeton.edu/webapps/portal/execute/defaultTab")
    print ("COOKIEJAR AFTER GOING BACK TO CAS "),
    print(cookiejar)    
    
    BBhtml = br.response().read()
    with open("lol.html", "w") as lol:
        lol.write(BBhtml)