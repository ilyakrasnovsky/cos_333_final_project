from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect

import backend

from .forms import NameForm
from assigncal.models import DJStudent, DJCourse, Student, Course

def cal(request):
    #items = Item.objects.exclude(amount=0)
    #dict to send to template
    #context = {'items': items}
    backend.add_to_db({'name' : 'string', 'payload' : 'stuff'})
    #context = {'items' : backend.get_from_db('string')}
    #path starts at project/templates/
    return render(request, 'assigncal/cal.html')

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
