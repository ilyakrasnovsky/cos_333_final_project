from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings

import backend
import CASClient
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
    
    #Make DJStudent (Django model) object out of netid
    DJSobject = Sobject.djangofy()
    
    #Add DJStudent to sqllite3 database (check for collisions)
    try:
        DJStudent.objects.get(netid=netid)
    except DJStudent.DoesNotExist, DJStudent.MultipleObjectsReturned:
        DJSobject.save()
    #print (DJStudent.objects.get(netid=netid).netid)

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
    # scrape courses
    for course in courses:
        c = regexp3.search(course)
        if (c != None):
            courselist.append(c.group(0))

    for course in courselist:
        course = course.split('>')[1]
        course = course.split('<')[0]
        print(course)

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
        driver.find_element_by_link_text("Assignments").click()

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

        for a in assignmentlinks:
            name = regexp3.search(a)
            link = regexp4.search(a)
            if (name != None):
                name = (name.group(0)).split('>')[2]
                name = name.split('<')[0]
            if (link != None):
                link = (link.group(0)).split('"')[1]
                link = link.split('"')[0]

            if "Sol" not in a:
                print (name,link)

    driver.close()

    # idk where to return to rn
    return HttpResponseRedirect(url)

    
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
