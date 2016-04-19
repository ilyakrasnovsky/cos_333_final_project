from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings

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
    context = {'title' : "DjangoAlex"}
    return render(request, 'assigncal/cal.html', context)

@ensure_csrf_cookie
def save(request):
    if (request.method == 'POST'):
        #backend.add_to_db({"name" : "lol", "payload": request.POST.dict()})
        return render(request, 'assigncal/cal.html')

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
    
    return HttpResponseRedirect("https://blackboard.princeton.edu/")
    
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
