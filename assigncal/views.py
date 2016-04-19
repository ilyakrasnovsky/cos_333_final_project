from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.http import JsonResponse

import backend
import CASClient
import re
import mechanize

from .forms import NameForm
from assigncal.models import DJStudent, DJCourse, Student, Course

SITE_URL = settings.SITE_URL

@ensure_csrf_cookie
def cal(request):
    #items = Item.objects.exclude(amount=0)
    #dict to send to template
    #context = {'items': items}
    #backend.add_to_db({'name' : 'string', 'payload' : 'stuff'})
    #context = {'items' : backend.get_from_db('string')}
    #path starts at project/templates/
    return render(request, 'assigncal/cal.html')

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
        return render(request, 'assigncal/cal.html')

#remove free time blocks from users freelist
@ensure_csrf_cookie
def remove(request):
    if (request.method == 'POST'):
        Sdict = backend.getStudent(request.session.get('netid'))['freedict']
        toRemove = makeFreeList(request.POST.dict()['starttime'],
                              request.POST.dict()['endtime'])
        for i in toRemove.keys():
            Sdict.pop(i, None)
        backend.forceUpdateStudent(request.session.get('netid'), {"freedict" : Sdict})
        return render(request, 'assigncal/cal.html')

def eventfeed(request):
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
    #Redirect to CAS login, will append ticket in response
    C = CASClient.CASClient(SITE_URL)
    login_url = C.Authenticate()
    return HttpResponseRedirect(login_url)

def gotoBB(request):
    #Pull ticket from request url
    requrl = request.get_full_path()
    ticket = re.split("ticket=",requrl)[1]
    
    #Validate ticket, get netid from it
    C = CASClient.CASClient(SITE_URL)
    netid = C.Validate(ticket)

    #Save netid to session for use in other views
    request.session['netid'] = netid

    #Make Student object out of netid    
    Sobject = Student(netid)
    
    #Add dictified Student object to firebase
    backend.addStudent(Sobject.dictify())
    
    '''
    #Make DJStudent (Django model) object out of netid
    DJSobject = Sobject.djangofy()
    
    #Add DJStudent to sqllite3 database (check for collisions)
    try:
        DJStudent.objects.get(netid=netid)
    except DJStudent.DoesNotExist, DJStudent.MultipleObjectsReturned:
        DJSobject.save()
    #print (DJStudent.objects.get(netid=netid).netid)
    '''
    
    #Automated scraping and browsing of blackboard called here
    br = mechanize.Browser()
    br.open("https://blackboard.princeton.edu/")
    BBhtml = br.response().read()
    #print (BBhtml)
    return render(request, 'assigncal/cal.html')    
    #return HttpResponseRedirect("https://blackboard.princeton.edu/")
    
'''
def item_detail(request, id):
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        raise Http404('This item does not exist')
    context = {'item' : item}
    return render(request, 'inventory/item_detail.html', context)

def entry(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            #save it as model in SQLlite
            #NEED TO CHECK FOR COLLISIONS
            newname = UName(name = form.cleaned_data['your_name'])
            newname.save()
            # redirect to a new URL:
            #return HttpResponseRedirect('/thanks/', user=newname.name)
            #render a different html on this URL (different things!)
            name = UName.objects.get(name=newname.name)
            context = {'name' : name.name}
            return render(request, 'inventory/thanks.html', context)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    context = {'form' : form}
    return render(request, 'inventory/entry.html', context)

def thanks(request, user):
    name = UName.objects.get(name=user)
    context = {'name' : name.name}
    return render(request, 'inventory/thanks.html', context)
'''
