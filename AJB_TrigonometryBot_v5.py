# @abrightmoore - see @TrigonometryBot
# This version refactored for extensibility
# - replace PyGame with PIL for image manipulation

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from markovbot import MarkovBot # by @esdalmaijer. Use for conversation
from TwitterAPI import TwitterAPI # by @boxnumber03 https://dev.twitter.com/resources/twitter-libraries. Wrapper to communicate via Twitter
import os
import time
from random import randint, random, Random
import io
import sys
from io import BytesIO
from PIL import Image
# import pygame, sys
# from pygame.locals import *
DEBUGMAX = False # Disable
DEBUGLOGMETHODCALLS = True
DEBUGLOGMETHODCALLSNESTED = False
TWITTERLIMIT = 140 # Characters
jobsComplete = 0

GAMENAME = "AJB_TrigonometryBot"
GAMEVER = 4.0
FILENAMEIMAGE = '@abrightmoore_@TrigonometryBot_output.png'
MYNAME = "@TrigonometryBot"

def mainLoop():
	if DEBUGLOGMETHODCALLS == True: print "mainLoop()"
	# Init
	api = connectToTwitter()
	tweetbot = initMarkovBot() # Required for supporting conversations
	tweetPrefixDefault = "@abrightmoore, I made this. "
	max_ids = loadStringsFromFile(GAMENAME,"MAXID.txt")
#	maxidfile = open(GAMENAME+"_"_MAXID.txt', 'r+')
#	max_ids = [int(x) for x in maxidfile.read().split()]
	# print max_ids
	max_id = int(max_ids[len(max_ids)-1])
	# print str(max_id)+" (max_id)"
#	maxidfile.close()
	
	R = Random()
	if len(sys.argv) > 1: # Passed a seed
		try:
			R = Random(int(sys.argv[1]))
		except:
			print "Unable to determine seed from: "+sys.argv[1]

	width = 400
	if len(sys.argv) > 2:
		try:
			width = int(sys.argv[2]) # Pixels wide and tall
		except:
			print "Unable to determine width from: "+sys.argv[2]
	height = width

	iAmAwake = True
	sleeps = 0 # a count of 'days'
	restTimeDefault = 15 # Seconds.
	restTimeMax = 120
	restTime = restTimeDefault # when it is time to sleep, how long to sleep for
	moodCreative = 0.01 # How likely I will create _something_ when tested
	jobsComplete = 0
	# Wake periodically and decide what to do
	while iAmAwake == True:
		# Either pro-actively work on something creative or otherwise check what people have sent through
		if random() <= moodCreative:
			newFile = createImgFile(R,height,width) # Create something
			# To Do: Adjust image based on 'mood' or how 'tired' I am
			tweet_text = getTweetText(tweetbot,tweetPrefixDefault,SEEDWORD)
			while len(tweet_text) > TWITTERLIMIT: # Twitter limit
				tweet_text = getTweetText(tweetbot,tweetPrefixDefault,SEEDWORD)
			print tweet_text
			postToTwitter_File(api,newFile,tweet_text)
			jobsComplete = jobsComplete +1
		# Poll Twitter for mentions
		max_id = handleMentions(api,R,max_id,tweetbot)
		
		# Go to sleep - duration depends on jobs completed this cycle
		restTime = restTime+restTimeDefault*jobsComplete
		if restTime > restTimeMax:
			restTime = restTimeMax
		iAmAwake = False
		print "Sleeping for "+str(restTime)+" seconds"
		time.sleep(restTime)
		
		# Post sleep processing
		sleeps = sleeps+1
		iAmAwake = True
		moodCreative = 0.01
		# jobsComplete = 0

# STATIC STRINGS AND OTHER THINGS

def loadStringsFromFile(filePrefix,fileSuffix):
	if DEBUGLOGMETHODCALLS == True: print "loadStringsFromFile("+filePrefix+","+fileSuffix+")"
	fileName = filePrefix+"_"+fileSuffix
	fileOfStatements = open(fileName, 'r+')
	keys = fileOfStatements.read().split()
	fileOfStatements.close()
	if DEBUGMAX: print keys # Debug - remove for security
	return keys
		
# CONVERSATION MANAGEMENT

def getTweetText(tweetbot,prefix,seedword):
	if DEBUGLOGMETHODCALLS == True: print "getTweetText(tweetbot,"+prefix+",seedword)"
	TWEET_TEXT = STATEMENT[randint(0,len(STATEMENT)-1)] # Choose a pre-canned statement
	if random() > 0.2:
		TWEET_TEXT = tweetbot.generate_text(25, seedword)
	TWEET_TEXT = prefix+"\n"+TWEET_TEXT
	return TWEET_TEXT

def initMarkovBot():
	if DEBUGLOGMETHODCALLS == True: print "initMarkovBot()"
	tweetbot = MarkovBot()
	dirname = os.path.dirname(os.path.abspath(__file__))
	book = os.path.join(dirname,'book.txt')
	tweetbot.read(book)
	return tweetbot	
	
# IMAGE MANIPULATION

def makeTrigImage(R,img,formulaR,formulaG,formulaB): # A kind of psychedelic picture based on application of formula across each location on a place.
	if DEBUGLOGMETHODCALLS == True: print "makeTrigImage(R,img,"+formulaR+","+formulaG+","+formulaB+")"

	width = img.size[0]
	height = img.size[1]

	a = 255
	cw = width>>1
	ch = height>>1
	scale = 0

	scaleDelta = 1
	if False:
		scaleDelta = -randint(1,(width+height)>>3)
		if R.random() > 0.5:
			scaleDelta = -scaleDelta
	QUANTUMX = (2.0*pi)/float(width*scaleDelta)
	QUANTUMY = (2.0*pi)/float(height*scaleDelta)

	pixels = img.load()
	for x in xrange(0,width):
		for y in xrange(0,height):
			px = QUANTUMX * float(x-cw)
			py = QUANTUMY * float(y-ch)
		
			r = calcFormula(formulaR,px,py)*127+127
			# print r
			g = calcFormula(formulaG,px,py)*127+127
			b = calcFormula(formulaB,px,py)*127+127
			if r > 255:
				r = 255
			elif r < 0:
				r = 0
			if g > 255:
				g = 255
			elif g < 0:
				g = 0                                           
			if b > 255:
				b = 255
			elif b < 0:
				b = 0                                           

			pixels[int(x),int(y)] = (int(r),int(g),int(b),int(a))
	

def createImgFile(R, width,height):
	if DEBUGLOGMETHODCALLS == True: print "createImgFile(R,"+str(width)+","+str(height)+")"

	# In memory file method used is by Rolo http://wildfish.com/blog/2014/02/27/generating-in-memory-image-for-tests-python/
	img = Image.new('RGBA', size=(width, height), color=(0, 0, 0))

	# Choose what type of image to create
	if True:
		(formulaR,formulaG,formulaB) = getFormulas(R)
		makeTrigImage(R,img,formulaR,formulaG,formulaB)
	
	file = BytesIO()	
	img.save(file, 'png')
	file.name = FILENAMEIMAGE
	file.seek(0)
	return file # Twitter works with files 

def createImgFileWithRules(R,width,height,ruleRed,ruleGreen,ruleBlue):
	if DEBUGLOGMETHODCALLS == True: print "createImgFileWithRules(R,"+str(width)+","+str(height)+","+ruleRed+","+ruleGreen+","+ruleBlue+")"

	# In memory file method used is by Rolo http://wildfish.com/blog/2014/02/27/generating-in-memory-image-for-tests-python/
	img = Image.new('RGBA', size=(width, height), color=(0, 0, 0))

	# Choose what type of image to create
	if True:
		(formulaR,formulaG,formulaB) = (ruleRed,ruleGreen,ruleBlue)
		makeTrigImage(R,img,formulaR,formulaG,formulaB)
	
	file = BytesIO()	
	img.save(file, 'png')
	file.name = FILENAMEIMAGE
	file.seek(0)
	return file # Twitter works with files 
	
# TWITTER ACCESS

def postToTwitter_File(api,newFile,tweet_text):
	if DEBUGLOGMETHODCALLS == True: print "postToTwitter_File(api,newFile,"+tweet_text+")"
	# STEP 1 - upload image
	data = newFile.read()
	r = api.request('media/upload', None, {'media': data})
	print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE')

	# STEP 2 - post tweet with a reference to uploaded image
	if r.status_code == 200:
		media_id = r.json()['media_id']
		r = api.request('statuses/update', {'status':tweet_text, 'media_ids':media_id})
		print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE')	

def handleMentions(api,R,max_id,tweetbot):
	if DEBUGLOGMETHODCALLS == True: print "handleMentions(api,R,"+str(max_id)+",tweetbot)"
	# Read the Twitter queue for messages, and process them
	
	jobsComplete = 0

	r = None
	if max_id != 0:
		# print max_id
		r = api.request('statuses/mentions_timeline', {'count':1,'since_id':max_id})
	else:
		r = api.request('statuses/mentions_timeline', {'count':20})
	print('Message poll complete' if r.status_code == 200 else str(r.status_code))
	if r.status_code == 200:
		for status in r:
			id = status["id"]
			# print "id: "+str(id)

			print "%s (%s) %s by %s" % (status["id"],status["created_at"], status["text"].encode("ascii", "ignore"), status["user"]["screen_name"])
			replyToName = "@"+status["user"]["screen_name"]
			# Oh excitement! I've been mentioned! Parse the message, create functions and an image, and reply
			msg = status["text"].encode("ascii", "ignore")
			
			if replyToName in ADMIN:
				# Check if an Admin command has been issued
				doNothing = True
				
			pos = msg.find("Rule") # Force render a picture
			if pos > 0:
				posR = msg.find("R:")
				posG = msg.find("G:")
				posB = msg.find("B:")
				if posR > 0 and posG > 0 and posB > 0 and posB > posG > posR:
					formulaR = msg[posR+2:posG-1]
					formulaG = msg[posG+2:posB-1]
					formulaB = msg[posB+2:]
					newFile = createImgFileWithRules(R,800,800,formulaR,formulaG,formulaB) # Create something
					tweet_text = replyToName+"\nHere is the image from\nR: "+formulaR+"\nG: "+formulaG+"\nB: "+formulaB
					print tweet_text
					postToTwitter_File(api,newFile,tweet_text)
			else:
				# Respond with a new picture
				# Strip out the username
				msg.replace(replyToName,"")
				msg.replace(MYNAME,"")
				msg.replace("@","") # 2017-02-05 AB - ensure formula munging doesn't spam random Twitter handles
				msg.strip()
				l = len(msg)-1
				print "Message: "+msg+"\nLength: "+str(l)
				# First pass...
				formulaR = msg[:-int(l/3)*2].strip()
				formulaG = msg[int(l/3)+1:-int(l/3)].strip()
				formulaB = msg[int(l/3)*2:].strip()
				if random() > 0.8:
					(formulaR,formulaG,formulaB) = getFormulas(R)
				# Whittle a little: make the formulas a bit more compact

				if len(formulaR) > 1:
					formulaR = formulaR[randint(1,len(formulaR)-1):].strip()
				if len(formulaG) > 1:
					formulaG = formulaG[randint(1,len(formulaG)-1):].strip()
				if len(formulaB) > 1:
					formulaB = formulaB[randint(1,len(formulaB)-1):].strip()

				print "R: "+formulaR
				print "G: "+formulaG
				print "B: "+formulaB
				
				img = Image.new('RGBA', size=(640, 480), color=(0, 0, 0))

				# Choose what type of image to create
				if True:
					# (formulaR,formulaG,formulaB) = getFormulas(R)
					makeTrigImage(R,img,formulaR,formulaG,formulaB)
				
				newFile = BytesIO()	
				img.save(newFile, 'png')
				newFile.name = FILENAMEIMAGE
				newFile.seek(0)

				# parse the original message for words to use in replying
				seedword = msg.split()
				
				tweet_text = getTweetText(tweetbot,replyToName+" R: "+formulaR+" G: "+formulaG+" B: "+formulaB,seedword) # Conversation management goes here
				
				while len(tweet_text) > TWITTERLIMIT: # Twitter limit
					tweet_text = getTweetText(tweetbot,replyToName,seedword)
				print tweet_text
				postToTwitter_File(api,newFile,tweet_text)

				r = api.request('favorites/create', {'id':id})
				print('FAVORITE SUCCESS' if r.status_code == 200 else 'FAVORITE FAILURE')
					
				jobsComplete = jobsComplete +1

			if id > max_id:
				max_id = id
				addStringToFile(GAMENAME,'MAXID.txt',str(max_id))
				#maxidfile = open('./TrigonometryBot_MAXID.txt', 'a+')
				#maxidfile.write("\n"+str(id))
				#maxidfile.close()
			if replyToName not in ACQUAINTANCE:
				addStringToFile(GAMENAME,"Acquaintances.txt",replyToName)
				ACQUAINTANCE.append(replyToName)
				
	return max_id
	
def addStringToFile(prefix,suffix,theString):
	theFile = open(prefix+'_'+suffix, 'a+')
	theFile.write("\n"+str(theString))
	theFile.close()
	
def loadTwitterKeysFromFile(filePrefix):
	if DEBUGLOGMETHODCALLS == True: print "loadTwitterKeysFromFile("+filePrefix+")"
	fileName = filePrefix+"_TwitterKeys.txt"
	fileOfKeys = open(fileName, 'r+')
	keys = fileOfKeys.read().split()
	fileOfKeys.close()
	if DEBUGMAX: print keys # Debug - remove for security
	return (keys[0],keys[1],keys[2],keys[3])

def connectToTwitter():
	if DEBUGLOGMETHODCALLS == True: print "connectToTwitter()"
	# Load keys from file, connect to Twitter using them.
	(cons_key, cons_secret, access_token, access_token_secret) = loadTwitterKeysFromFile(GAMENAME)
	api = TwitterAPI(cons_key,cons_secret,access_token,access_token_secret) # Does this need to be retried?
	return api
	
# Process functions
def getFormulas(R):
	if DEBUGLOGMETHODCALLS == True: print "getFormulas(R)"

	formulaR = makeRandomFormula(R)
	print "  Red: "+formulaR
	formulaG = makeRandomFormula(R)
	print "Green: "+formulaG
	formulaB = makeRandomFormula(R)
	print " Blue: "+formulaB
	return (formulaR,formulaG,formulaB)

def makeRandomFormula(R):
	if DEBUGLOGMETHODCALLS == True: print "makeRandomFormula(R)"
	result = ""
	funcs = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRS"
	iters = R.randint(1,11)
	for i in xrange(0,iters):
		result=result+(funcs[R.randint(0,len(funcs)-1)])
	return result
	
def calcFormula(formula,x,y):
	if DEBUGLOGMETHODCALLSNESTED == True: print "calcFormula("+formula+","+str(x)+","+str(y)+")"
	# parse formula, substitute parameters, adjust result
	val = 1.0
	err = 0
	for c in formula:
		if c == "a":
			val = val* sin(y)
		elif c == "b":
			val = val* cos(y)
		elif c == "c":
			try:
				val = val* tan(y)
			except:
				err = err+1
				#print "Unable to calculate tan("+str(y)+")"
		elif c == "d":
			val = val* sin(x)
		elif c == "e":
			val = val* cos(x)
		elif c == "f":
			try:
				val = val* tan(x)
			except:
				err = err+1
				#print "Unable to calculate tan("+str(x)+")"
		elif c == "g":
			val = val* sin(x+y)
		elif c == "h":
			val = val* cos(x+y)
		elif c == "i":
			try:
				val = val* tan(x+y)
			except:
				err = err+1
				#print "Unable to calculate tan("+str(x)+"+"+str(y)+")"
		elif c == "j":
			val = val* sin(x-y)
		elif c == "k":
			val = val* cos(x-y)
		elif c == "l":
			try:
				val = val* tan(x-y)
			except:
				err = err+1
				#print "Unable to calculate tan("+str(x)+"-"+str(y)+")"
		elif c == "m":
			if y != 0:
				val = val* x/y
		elif c == "n":
			if x != 0:
				val = val* y/x
		elif c == "o":
			val = val* (x-y)
		elif c == "p":
			val = val* (x+y)
		elif c == "q":
			val = val* x*y
		elif c == "r":
			val = val* atan2(y,x)
		elif c == "s":
			val = val* x**2 
		elif c == "t":
			val = val* x**3 
		elif c == "u":
			try:
				val = val* asin(x)
			except:
				err = err+1
		elif c == "v":
			try:
				val = val* acos(x)
			except:
				err = err+1
		elif c == "w":
			try:
				val = val* atan(x)
			except:
				err = err+1
				#print "Unable to calculate tan("+str(x)+")"
		elif c == "x":
			try:
				val = val* hypot(x,y)
			except:
				err = err+1
		elif c == "y":
			try:
				val = val* acosh(x)
			except:
				err = err+1
		elif c == "z":
			try:
				val = val* asinh(x)
			except:
				err = err+1
		elif c == "A":
			try:
				val = val* atanh(x)
			except:
				err = err+1
		elif c == "B":
			try:
				val = val* cosh(x)
			except:
				err = err+1
		elif c == "C":
			try:
				val = val* sinh(x)
			except:
				err = err+1
		elif c == "D":
			try:
				val = val* tanh(x)
			except:
				err = err+1
		elif c == "E":
			val = val* min(x,y)
		elif c == "F":
			val = val* max(x,y)

		elif c == "G":
			val = val* sin(val)
		elif c == "H":
			val = val* cos(val)
		elif c == "I":
			try:
				val = val* tan(val)
			except:
				err = err+1
		elif c == "J":
			val = val**2
		elif c == "K":
			try:
				val = val* asin(val)
			except:
				err = err+1
		elif c == "L":
			try:
				val = val* acos(val)
			except:
				err = err+1
		elif c == "M":
			try:
				val = val* atan(val)
			except:
				err = err+1
		elif c == "N":
			try:
				val = val* acosh(val)
			except:
				err = err+1
		elif c == "O":
			try:
				val = val* asinh(val)
			except:
				err = err+1
		elif c == "P":
			try:
				val = val* atanh(val)
			except:
				err = err+1
		elif c == "Q":
			try:
				val = val* cosh(x)
			except:
				err = err+1
		elif c == "R":
			try:
				val = val* sinh(val)
			except:
				err = err+1
		elif c == "S":
			try:
				val = val* tanh(val)
			except:
				err = err+1
			
	return val
	
##################

STATEMENT = loadStringsFromFile(GAMENAME,"Statements.txt")
SEEDWORD = loadStringsFromFile(GAMENAME,"Seedwords.txt")
ADMIN = loadStringsFromFile(GAMENAME,"Admins.txt")
ACQUAINTANCE = loadStringsFromFile(GAMENAME,"Acquaintances.txt")
mainLoop()