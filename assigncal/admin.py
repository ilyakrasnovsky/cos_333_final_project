from django.contrib import admin
from .models import DJStudent, DJCourse

#Inherit from ModelAdmin over just model
class DJStudentAdmin(admin.ModelAdmin):
	list_display = ['netid', 'freelist']

#Inherit from ModelAdmin over just model
class DJCourseAdmin(admin.ModelAdmin):
	#specify what fields to show in admin mode
	list_display = ['name', 'students', 'duedates']

#Register the model Item and ItemAdmin 
admin.site.register(DJStudent, DJStudentAdmin)
#Register the model UName with UNameAdmin
admin.site.register(DJCourse, DJCourseAdmin)
