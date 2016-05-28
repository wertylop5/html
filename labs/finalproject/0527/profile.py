#!/usr/bin/python
#TODO include \n in posts, make upvote/downvote blah
import Cookie,os,cgi,pickle,sys,cgitb,hashlib

cgitb.enable()

sys.path.insert(0, "../modules")
import stdStuff

head = '''<!DOCTYPE html>
<html>
<head><title>Profile</title>
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

splitChar = chr(182)
splitPost = chr(208)

#gordons code
def poster():
	return '''<form action = "profile.py" method = "GET">
Title: <input name="postTitle" type="textfield">
<br>
Text: <textarea name="textBody" rows="10" cols="15">
</textarea>
<br>
<input type = "submit" value = "Make Post">
</form>'''

def writePost(cookie, formThing):
	countStream = open(stdStuff.directory + stdStuff.counterFile, "r")
	counter = int(countStream.read())
	countStream.close()
	
	postWStream = open(stdStuff.directory + stdStuff.postFile, "ab")
	pickle.dump(stdStuff.Post(counter, 
							cookie["username"].value,
							formThing.getvalue("postTitle"),
							formThing.getvalue('textBody')),
				postWStream)
	postWStream.close
	
	counter += 1
	countWStream = open(stdStuff.directory + stdStuff.counterFile, "w")
	countWStream.write(str(counter))
	countWStream.close()

def makeTag(tag, text):
	return "<" + tag + ">" + str(text) + "</" + tag + ">"

#reads in posts
def displayPost(postObj, titleTag, bodyTag, userTag, commentTag=""):
	postResult = ""
	
	postResult += """<table>
<tr>
	<td>""" + str(postObj.score) + """</td>
	<td>
"""
	
	postResult +=	makeTag(userTag, postObj.id) + \
					makeTag(userTag, postObj.user) + \
					makeTag(titleTag, postObj.title) + \
					makeTag(bodyTag, postObj.text)
	
	postResult += "<a href='profile.py?downVote=lol&postId="+\
	str(postObj.id) + "'>Down Vote</a><br>"
	
	postResult += "<a href='profile.py?upVote=lol&postId="+\
	str(postObj.id) + "'>Up Vote</a><br>"
	
	postResult += """<a href='postExpanded.py?expandButton=""" + \
	str(postObj.id) + "'>Comment </a>"
	
	postResult += """</td>
	</tr>
</table>
"""
	
	return postResult

def makePage():
	res = str(poster())
	
	#not sure why it doesnt work
	postList = stdStuff.objFileToList(stdStuff.directory, stdStuff.postFile)
	#print len(postList)
	for post in postList:
		res += displayPost(post, "h1", "p", "h6")
	
	return res


'''
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
			### PUT PAGE STUFF HERE
			body += """<form method="GET" action="homepage.py">
<input name="logOut" type="submit" value="Log out">
</form>
"""
			if "postTitle" in form:
				writePost(c, form)
			
			allPosts = []
			if "downVote" in form or "upVote" in form:
				targId = form.getvalue("postId")
				allPosts = stdStuff.objFileToList(stdStuff.directory,
											stdStuff.postFile)
				if "downVote" in form:
					for index, value in enumerate(allPosts):
						if value.id == targId:
							allPosts[index].decreaseScore()
							break
				elif "upVote" in form:
					for index, value in enumerate(allPosts):
						if value.id == targId:
							allPosts[index].increaseScore()
							break
				allPosts = stdStuff.objFileToList(stdStuff.directory,
										 stdStuff.postFile)
				
				
				tempy = open(stdStuff.directory + stdStuff.postFile, "wb")
				for x in allPosts:
					pickle.dump(x, tempy)
				tempy.close()
			
			
			body+=makePage()
		else:
			body+="Failed to Authenticate cookie<br>\n"
			body+= 'Go Login <a href="login.py">here</a><br>'
	else:
		body+= "Your information expired<br>\n"
		body+= 'Go Login <a href="login.py">here</a><br>'
else:
	body+= 'You seem new<br>\n'
	body+='Go Login <a href="login.py">here</a><br>'
'''

print 'content-type: text/html'
print ''



print head

body += """<form method="GET" action="homepage.py">
<input name="logOut" type="submit" value="Log out">
</form>
"""
if "postTitle" in form:
	writePost(c, form)

allPosts = []
if "downVote" in form or "upVote" in form:
	targId = form.getvalue("postId")
	allPosts = stdStuff.objFileToList(stdStuff.directory,
								stdStuff.postFile)
	#print len(allPosts)
	if "downVote" in form:
		for index, value in enumerate(allPosts):
			if value.id == targId:
				print "found"
				allPosts[index].decreaseScore()
				break
	elif "upVote" in form:
		for index, value in enumerate(allPosts):
			if value.id == targId:
				allPosts[index].increaseScore()
				break
	allPosts = stdStuff.objFileToList(stdStuff.directory,
							 stdStuff.postFile)
	
	
	tempy = open(stdStuff.directory + stdStuff.postFile, "wb")
	for x in allPosts:
		print x.score
		pickle.dump(x, tempy)
	tempy.close()
body+=makePage()
print body
print foot
