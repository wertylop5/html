#!/usr/bin/python
print "content-type: text/html\n"

import sys
sys.path.insert(0, "../modules")
import htmlFuncts
from htmlFuncts import *
import dataToTable
import sortAlg

g_distinctWords = 0
g_totWords = 0

def TallyWords(text):
	global g_distinctWords
	global g_totWords
	g_totWords = 0
	#Converted form
	textList = []
	
	#special case for dante: remove double dashes
	text = " ".join(text.split("--"))
	
	#remove whitespace
	textList = text.split()
	
	#stores useless punctuation, need extra test for apostrophe
	punct = ["!", "?", ":", ";", "/", ",", ".", \
	'"', "(", ")", "-", "[", "]", "<", ">"]
	punctStr = '''!?:;/,."'()-[]<>@#$%^&*'''
	
	#so stuff isn't too long
	q = ""
	#(smartly) removes punctuation
	for x in range(0, len(textList)):
		q = textList[x]
		
		if len(q) > 0:
			q = q.strip(punctStr)
			#prelim check for special case of ' after a "s"
			if len(q) > 2:
				if q[len(q) - 2] == "s" and q[len(q) - 1] == "'":
					q += "!"
					q = q.strip("'").strip("!")
				#else:
			#q = q.strip("'")
			textList[x] = q
	
	for x in range(len(textList)):
		textList[x] = textList[x].lower()
	
	#Stores index of existing word in hits
	tempIndex = 0
	
	#now with dictionaries!!1!1!
	tallies = {}
	
	for x in textList:
		if len(x) > 0:
			g_totWords += 1
			if not(x in tallies.keys()):
				tallies[x] = 1
				
				g_distinctWords += 1
			else:
				tallies[x] += 1
	return tallies

#go through a
#if x not in b, then put into b with value 0
def fillMissing(a, b):
	for x in a.keys():
		if not(x in b.keys()):
			b[x] = 0

def makeSubList(name, dictOne, dictTwo, count1, count2, key):
	temp = []
	temp.append(name)
	
	#percentages
	temp.append(
				str(
				abs(
				round(
				(((dictOne[key] / float(count)) * 100) -
				((dictTwo[key] / float(count2)) * 100)),
				4)
				)
				) + "%"
				)
	return temp

#list of lists
#format: [["word", 5], ["two", 0]]
#dictOne is required

#one arg returns that as a list of lists
#two arg returns words, but numbers are subtracted
def dictToList(	dictOne, 
				totalCount, 
				dictOneName = "",
				totalCount2 = 0,
				dictTwo = None,
				dictTwoName = ""):
	res = []
	temp = []
	keyStore = []
	keyStore = dictOne.keys()
	keyStore.sort()
	
	#fun stuff, only 2 columns
	#first column is higher book name instead of word
	#second is difference in percentage
	if dictTwo:
		for x in keyStore:
			if dictOne[x] > dictTwo[x]:
				temp = makeSubList(dictOneName,
						dictTwo, dictOne, totalCount2, totalCount, x)
			else:
				temp = makeSubList(dictTwoName,
						dictOne, dictTwo, totalCount, totalCount2, x)
			res.append(temp)
			temp = []
	else:
		for x in keyStore:
			temp.append(x)
			temp.append(dictOne[x])
			temp.append(
						str(
						abs(
						round(
						((dictOne[x] / float(totalCount)) * 100),
						4)
						)
						) +"%"
						)
			
			res.append(temp)
			temp = []
	return res

def strToList(s):
	res = []
	for x in s:
		res.append(x)
	return res

#returns an inverted copy of the list
def invertDict(d):
	res = {}
	
	#for dupe handling
	carry = 0
	letter = ord('a')
	tempKey = ""
	
	for x in d.keys():
		if not(d[x] in res):
			res[ d[x] ] = x
		#fun stuff
		else:
			tempKey = str(d[x])
			#puts a carry # of z before the letter
			if letter > ord('z'):
				letter = ord('a')
				carry += 1
			tempKey += ('z' * carry) + chr(letter)
			print tempKey
			letter += 1
			
			res[tempKey] = x
	return res

def mostCommon(dictX, keyOut, valOut):
	dictTemp = invertDict(dictX)
	#values is numbers, keys is words
	values = []
	keys = []
	
	#for extracting numbers from dupes
	tempChar = ""
	tempPos = 0
	tempList = []
	tempNum = 0
	
	#for making the final number
	counter = 1
	
	
	for x in dictTemp.keys():
		if x.isdigit():
			values.append(int(x))
			keys.append(dictTemp[x])
		#handle the tailing letters
		else:
			while tempPos < len(x) and x[tempPos].isdigit():
				tempChar = x[tempPos]
				tempPos += 1
				tempList.append(tempChar)
			tempPos = 0
			
			while len(tempList) > 0:
				 tempNum += int(l.pop()) * (10 ** counter)
				 counter += 1
			counter = 1
			
			values.append(tempNum)
			keys.append(dictTemp[x])
	keyOut.extend(keys)
	valOut.extend(values)

########################################## Stream stuff
filename = "hamlet.txt"
fileStream = open("res/" + filename, "r")
fileText = fileStream.read()
fileStream.close()

filename2 = "othello.txt"
fileStream2 = open("res/" + filename2, "r")
fileText2 = fileStream2.read()
fileStream2.close()
########################################## End Stream stuff
tally = TallyWords(fileText)
count = g_totWords
tally2 = TallyWords(fileText2)
count2 = g_totWords

fillMissing(tally, tally2)
fillMissing(tally2, tally)

print htmlFuncts.startPage("Pair")


sortedKey = sorted(tally, key=tally.get, reverse=True)
sortedVal = []
for x in sortedKey:
	sortedVal.append(tally[x])


sortedKey2 = sorted(tally2, key=tally2.get, reverse=True)
sortedVal2 = []
for x in sortedKey2:
	sortedVal2.append(tally2[x])


################### TABLE START ###################
print "<table>"

print "<tr>"

print "hamlet most common"
print "<table border='1'>"
for x in range(20):
	print "<tr>"
	
	print "<td>" + str(sortedKey[x]) + "</td>"
	print "<td>" + str(sortedVal[x]) + "</td>"
	
	print "</tr>"

print "</table>"

print "</tr>"



print "<tr>"

print "othello most common"
print "<table border='1'>"
for x in range(20):
	print "<tr>"
	
	print "<td>" + str(sortedKey2[x]) + "</td>"
	print "<td>" + str(sortedVal2[x]) + "</td>"
	
	print "</tr>"

print "</table>"

print "</tr>"



print "<tr>"

#### First one
print "<td>"
print "hamlet"

print makeTabs(5) + '<table border="1">'

print "Unique words: " + str(count)
print dataToTable.makeTableBody(dictToList(tally, count))

print makeTabs(5) + '</table>'
print "</td>"


#### Second one
print "<td>"
print "othello"
print makeTabs(5) + '<table border="1">'

print "Unique words: " + str(count2)
print dataToTable.makeTableBody(dictToList(tally2, count2))

print makeTabs(5) + '</table>'
print "</td>"



print "<td>"
print "both"
print makeTabs(5) + '<table border="1">'

print dataToTable.makeTableBody(dictToList(tally, count, 
								"hamlet",
								count2,
								tally2,
								"othello"))

print makeTabs(5) + '</table>'
print "</td>"
print "</tr>"















print "</table>"
print htmlFuncts.endPage()



















