#!/usr/bin/python
print "content-type: text/html\n"
import sys
import cgitb
import cgi
sys.path.insert(0, "../modules")
import htmlFuncts

cgitb.enable()

print htmlFuncts.startPageN("Create an account")

form = cgi.FieldStorage()

print """
<form method="GET" action="createaccount.py">
	Username: <input name="username" type="textfield">
	<input name="done" type="submit" value="yay">
</form>
"""
if "done" in form:
	direct = "data/"
	data = "usernames.txt"
	userAppendStream = open(direct + data, "a")
	userWriteStream = open(direct + data, "w")
	userReadStream = open(direct + data, "r")
	
	usernameList = userReadStream.read()
	usernameList = usernameList.split("\n")
	
	if not(form.getvalue("username") in usernameList):
		userAppendStream.write(form.getvalue("username") + "\n")
	
	userAppendStream.close()
	userWriteStream.close()
	userReadStream.close()


print htmlFuncts.endPage()