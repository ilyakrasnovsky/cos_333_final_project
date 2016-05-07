from django.conf.urls import include, url
from django.contrib import admin
from assigncal import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'firstdjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #r means re
    #cascades down in order
    #extra params are passed
    url(r'^$', views.login, name='login'),
    url(r'^save', views.save, name='save'),
    url(r'^remove', views.remove, name='remove'),
    url(r'^cal', views.cal, name='cal'),
    url(r'^gotoBB', views.gotoBB, name='gotoBB'),
    url(r'^eventfeed', views.eventfeed, name='eventfeed'),
    url(r'^courses', views.courses, name='courses'),
    url(r'^email', views.email, name='email'),
    url(r'^sendemail', views.sendemail, name='sendemail'),
    url(r'^addClass', views.addClass, name='addClass'),
    url(r'^remClass', views.remClass, name='remClass'),
    url(r'^numCourses', views.numCourses, name='numCourses'),
    #<> --> named group
    #url(r'^item/(?P<id>\d+)/', views.item_detail, name = 'item_detail'),
    #url(r'^entry/', views.entry, name = 'entry'),
    #url(r'^admin/', include(admin.site.urls)),
]
