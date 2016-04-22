#!/usr/bin/python

from . import pycasclient
import cgi, os, urllib, re, sys

def main():

	CAS_SERVER  = "https://fed.princeton.edu/cas/login?locale=en"
	SERVICE_URL = "http://127.0.0.1:8000/login/CAS"

	#status, id, cookie = pycasclient.login(CAS_SERVER, SERVICE_URL, secure=0, opt="gateway")
	cookie = pycasclient.login(CAS_SERVER, SERVICE_URL, secure=0, opt="gateway")
	print "Content-type: text/html"
	print cookie
	print
	print """
	<html>
	<head>
	<title>
	castest.py
	</title>
	<style type=text/css>
	td {background-color: #dddddd; padding: 4px}
	</style>
	</head>
	<body>
	<h2>pycas.py</h2>
	<hr>
	"""
	#  Print browser parameters from pycas.login
	if cgi.FieldStorage().has_key("ticket"):
		ticket = cgi.FieldStorage()["ticket"].value
	else:
		ticket = ""

	in_cookie = os.getenv("HTTP_COOKIE")

	print """
	<p>
	<b>Parameters sent from browser</b>
	<table>
	<tr> <td>Ticket</td> <td>%s</td> </tr> 
	<tr> <td>Cookie</td> <td>%s</td> </tr> 
	</table>
	</p>""" % (ticket,in_cookie)


		#  Print output from pycas.login
	print """
	<p>
	<b>Parameters returned from pycas.login()</b>
	<table>
	<tr><td>status</td><td> <b>%s</b> - <i>%s</i></td></tr>
	<tr><td>id</td><td> <b>%s</b></td></tr>
	<tr><td>cookie</td><td> <b>%s</b></td></tr>
	</table>
	</p>
	</body></html>""" % (cookie,cookie,cookie,cookie) #(status,CAS_MSG[status],id,cookie)
