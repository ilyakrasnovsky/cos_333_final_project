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
    url(r'^$', views.cal, name='cal'),
    url(r'^save', views.save, name='save'),
    url(r'^login', views.login, name='login'),
    url(r'^gotoBB', views.gotoBB, name='gotoBB'),
    url(r'^myfeed', views.myfeed, name='myfeed'),
    #<> --> named group
    #url(r'^item/(?P<id>\d+)/', views.item_detail, name = 'item_detail'),
    #url(r'^entry/', views.entry, name = 'entry'),
    #url(r'^admin/', include(admin.site.urls)),
]
