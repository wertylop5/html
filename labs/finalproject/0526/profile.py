#!/usr/bin/python
#TODO maybe begin multiple users, include \n in posts
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




directory = "../data/"
userFile = "users.txt"
logFile = "loggedin.txt"
postFile = "posts.txt"
counterFile = "counter.txt"
commentFile = "comments.txt"


form = cgi.FieldStorage()

def authenticate(u,ID,IP):
    loggedIn = open(directory + logFile,'r').read().split('\n')
    loggedIn = [each.split(',') for each in loggedIn]
    loggedIn.remove([''])
    for a in loggedIn:
        if a[0] == username:
            return a[1]==str(ID) and a[2]==IP
    return False

#def makePage():
#	return """<form method="GET" action="makePost.py">
#	<input name="makePost" type="submit" value="Create a post">
#	</form>
#"""

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
	countStream = open(directory + counterFile, "r")
	counter = int(countStream.read())
	countStream.close()
	
	postWStream = open(directory + postFile, "a")
	pickle.dump(stdStuff.Post(counter, 
							cookie["username"].value,
							formThing.getvalue("postTitle"),
							formThing.getvalue('textBody')),
				postWStream)
	postWStream.close
	
	counter += 1
	countWStream = open(directory + counterFile, "w")
	countWStream.write(str(counter))
	countWStream.close()

def makeTag(tag, text):
	return "<" + tag + ">" + str(text) + "</" + tag + ">"

#reads in posts
#later: handle comments
def displayPost(postObj, titleTag, bodyTag, userTag, commentTag=""):
	postResult = ""
	postResult += 	makeTag(userTag, postObj.id) + \
					makeTag(userTag, postObj.user) + \
					makeTag(titleTag, postObj.title) + \
					makeTag(bodyTag, postObj.text)
	
	postResult += """<form method="GET" action="postExpanded.py">
<input name="expandButton" type="submit" value='""" + \
	str(postObj.id) + """'>
</form>"""
	
	return postResult

def makePage():
	res = str(poster())
	
	#not sure why it doesnt work
	postList = stdStuff.objFileToList(directory, postFile)
	'''
	postReadStream = open(directory + postFile, "rb")
	postList = []
	try:
		while True:
			postList.append(pickle.load(postReadStream))
	except EOFError:
		print "End of File"
	finally:
		postReadStream.close()
	'''
	
	for post in postList:
		res += displayPost(post, "h1", "p", "h6")
	
	return res



if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    c = Cookie.SimpleCookie()
    c.load(cookie_string)
    ##print all the data in the cookie
    #body+= "<h1>cookie data</h1>"
    #for each in c:
    #    body += each+":"+str(c[each].value)+"<br>"


    
    if 'username' in c and 'ID' in c:
        username = c['username'].value
        ID = c['ID'].value
        IP = os.environ['REMOTE_ADDR']
        
        if authenticate(username,ID,IP):
            body += """<form method="GET" action="homepage.py">
<input name="logOut" type="submit" value="Log out">
</form>
"""
			### PUT PAGE STUFF HERE
            if "postTitle" in form:
                writePost(c, form)
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

print 'content-type: text/html'
print ''

print head
print body
print foot
