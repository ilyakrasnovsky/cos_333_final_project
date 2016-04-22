'''
django models module
'''
from __future__ import unicode_literals

from django.db import models
import json

'''
class Student 

data structure for storing student data

attributes:
    netid : name of course (string, Ex. "COS 333")
    freelist : list of formatted strings of all free blocks (Ex.
               [2016-01-17T13:30:00, 2016-01-25T13:30:00])

initializer input:
    name (required)
    freelist (optional)

functions:
    DEPRECATED djangofy : method that returns a DJStudent()
                instance, which is the same data structure
                but inherits from django.models
    dictify : method that returns a dictionary
                representation of this instance (for json
                    conversion into firebase)
'''
class DJStudent(models.Model):
    netid = models.CharField(max_length=20)
    freelist = models.TextField()

class Student:
    def __init__(self, netid, freelist=None):
        self.netid = netid
        self.freelist = freelist

    def _djangofy(self):
        return  DJStudent(netid=self.netid,\
                 freelist=json.dumps(self.freelist))

    def dictify(self):
        return  {
                    "netid": self.netid,\
                    "freelist" : self.freelist\
                }
'''
class Course

data structure for storing class data

attributes:
    name : name of course (string, Ex. "COS 333")
    students : list of netids (strings, Ex. 
               [ilyak, amalleo, nmaselli, ghong] in this course)
    duedates : list of formatted strings of all due dates (Ex.
               [2016-01-17T13:30:00, 2016-01-25T13:30:00])

initializer input:
    name (required)
    students (optional)
    duedates (optional)

functions:
    DEPRECATED djangofy : method that returns a DJCourse()
                instance, which is the same data structure
                but inherits from django.models
    dictify : method that returns a dictionary
            representation of this instance (for json
                conversion into firebase)
'''
class DJCourse(models.Model):
    name = models.CharField(max_length=7)
    students = models.TextField(null=True)
    duedates = models.TextField(null=True)

class Course:
    def __init__(self, name, students=None, duedates=None):
        self.name = name
        self.students = students
        self.duedates = duedates

    def _djangofy(self):
        return  DJCourse(name=self.name,\
                 students=json.dumps(self.students),\
                 duedates=json.dumps(self.duedates))

    def _dictify(self):
        return  {
                    "name": self.name,\
                    "students" : self.students,\
                    "duedates" : self.duedates 
                }

'''
#EXAMPLE DJANGO MODEL
class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.IntegerField()
    #TEXT : CharField(max_length), TextField, EmailField, URLField
    #NUMBERS : IntegerField, DecimalField
    #FILES : FileField
    #IMAGES : ImageField
    #BOOLEAN : BooleanField
    #DATE/TIME : DateTimeField
    #ATTRIBUTES (null = true/false, max_length, blank, default, choices
    #MIGRATIONS CHANGE DB TO REFLECT MODEL CHANGES via makemigrations and migrate (--list)
'''
