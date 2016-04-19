
import re

#will take html file of homepage of Blackboard user and get course names 
#being taken during Spring 2016 semester
def ExtractCourses():

	html = open('sample.html','r').read()
	regexp1 = re.compile("Spring 2016.*?</div>", flags=re.DOTALL)
   	coursecontent = regexp1.search(html).group(0)
 

   	regexp2 = re.compile(">.*?_S2016.*?<")
   	courses = re.findall(regexp2,coursecontent)

   	regexp3 = re.compile("size=\"\d\">.*?<")
   	courselist = []
 	for course in courses:
 		c = regexp3.search(course)
 		if (c != None):
 			courselist.append(c.group(0))

 	for course in courselist:
 		course = course.split('>')[1]
 		course = course.split('<')[0]
 		print course



#From the assignment page, retrieve the links to PSET pdfs
def getAssignments():

	html = open('sampleassignments.html','r').read()
	regexp1 = re.compile("contentListItem.*?</div>", flags=re.DOTALL)
	listitems = re.findall(regexp1, html)

	#find all links in list
	regexp2 = re.compile("<a.*?</a>", flags=re.DOTALL)
	assignmentlinks = []
	for items in listitems:
		link = regexp2.search(items)
		if (link != None):
			assignmentlinks.append(link.group(0))

	#filter out links, exclude Solutions

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
				 
	        
#ExtractCourses()
getAssignments()
	
