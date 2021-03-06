#!/usr/bin/python
print 'content-type: text/html\n'
import Cookie,os,cgi,pickle,sys,cgitb,hashlib
cgitb.enable()

sys.path.insert(0, "../modules")
import stdStuff

head = '''<!DOCTYPE html>
<html>
<head>
<title>Add a friend</title>
<link rel="stylesheet" type="text/css" href="../style/addFriend.css">
</head>
<body>
   '''
body = ""
foot = '''
</body>
</html>
'''



form = cgi.FieldStorage()

def authenticate(u,ID,IP):
	loggedIn = open(stdStuff.directory + stdStuff.logFile,'r').read().split('\n')
	loggedIn = [each.split(',') for each in loggedIn]
	loggedIn.remove([''])
	for a in loggedIn:
		if a[0] == username:
			return a[1]==str(ID) and a[2]==IP
	return False

#gordons code
def poster():
	return '''
<div id="poster">
<form action = "addFriend.py" method = "GET">
Find a user: <input name="userTarget" type="textfield" value="Watch your casing!">
<br>
<input name="search" type="submit" value="Find User">
</form>
</div>'''

def displayInboxWidget(cookie):
	currentUser = cookie["username"].value
	userDict = stdStuff.objFileToList(stdStuff.directory,
								stdStuff.userFile, byName=True)
	
	res = \
"""
<div class="widget" id="inboxWidget">
	<table border='1'>
		<tr>
			<td>
				<a href="inbox.py">View messages</a>
			</td>
		</tr>
	</table>
</div>
"""
	return res

def displayGroupWidget(cookie):
	currentUser = cookie["username"].value
	userDict = stdStuff.objFileToList(stdStuff.directory,
								stdStuff.userFile, byName=True)
	
	res = \
"""
<div class="widget" id="groupWidget">
	<table border='1'>
		<tr>
			<td>
				<a href="groups.py">View groups</a>
			</td>
		</tr>
	</table>
</div>
"""
	return res

def findUsers(usernameQuery, userDict, currentUser):
	hits = []
	for user in userDict:
		if not(user in userDict[currentUser].friends):
			if usernameQuery in user:
				hits.append(user)
	
	hits.sort()
	return hits

def displayUserList(usernameQuery, userDict, currentUser):
	res = ""
	res += "<div id='userList'><h2>Available users</h2>"
	res += """<form method="GET" action="addFriend.py">"""
	userList = findUsers(usernameQuery, userDict, currentUser)
	for user in userList:
		if user != currentUser:
			res += user + "<input name='" + user + "' type='checkbox'>"
			res += "<br>"
	
	res += "<br><br><br>"
	res += "<input name='requestFriend' type='submit' value='Add selected friends'>"
	res += """</form>
</div>"""
	return res

def sendFriendRequest(form, userDict, srcUser):
	res = "<div id='request'><h4>Request sent to: "
	atLeastOne = False
	for element in form:
		if element == srcUser:
			res += "<h2>You can't add yourself!</h2>"
		elif element in userDict:
			#send the friend request
			userDict[srcUser].inbox.sendMessage(element, "", "", request=True)
			atLeastOne = True
			res += element + ", "
	res = res[:len(res) - 2]
	res += "</h4></div>"
	if not(atLeastOne):
		res = "<div id='request'><h2>You didn't select anyone!</h2></div>"
	userDict = stdStuff.objFileToList(stdStuff.directory, 
									stdStuff.userFile, byName=True)
	return res
	

def makePage(cookie):
	res = ""
	res += displayInboxWidget(cookie)
	res += displayGroupWidget(cookie)
	res += poster()
	return res




if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c = Cookie.SimpleCookie()
	c.load(cookie_string)
	##print all the data in the cookie
	#body+= "<h1>cookie data</h1>"
	#for each in c:
	#	body += each+":"+str(c[each].value)+"<br>"


	
	if 'username' in c and 'ID' in c:
		username = c['username'].value
		ID = c['ID'].value
		IP = os.environ['REMOTE_ADDR']
		
		if authenticate(username,ID,IP):
			currentUser = c["username"].value
			userDict = stdStuff.objFileToList(stdStuff.directory,
								stdStuff.userFile, byName=True)
			body += "<div id='userHeader'>"
			body += """
<div id="username">
	<p>Logged in as: """ + \
username + \
"""</p>
</div>"""
			body += """
<div id="userButtons">
	<form method="GET" action="homepage.py">
		<input name="logOut" type="submit" value="Log out">
	</form>
	<a href="profile.py">Go back to profile</a>
</div>
</div>
"""
			#for the fixed post
			body += "<div id='userHeader2'></div>"
			
			
			body += makePage(c)
			if "search" in form:
				body += displayUserList(stdStuff.deleteBrackets(
												form.getvalue("userTarget")),
										userDict, currentUser)
			if "requestFriend" in form:
				body += sendFriendRequest(form, userDict, currentUser)

		else:
			body+="Failed to Authenticate cookie<br>\n"
			body+= 'Go Login <a href="login.py">here</a><br>'
	else:
		body+= "Your information expired<br>\n"
		body+= 'Go Login <a href="login.py">here</a><br>'
else:
	body+= 'You seem new<br>\n'
	body+='Go Login <a href="login.py">here</a><br>'


print head
print body
print foot







