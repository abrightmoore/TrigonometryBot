# @abrightmoore - see @TrigonometryBot
# This version refactored for extensibility

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
import os
import time
from random import randint, random, Random
import io
from io import BytesIO
import sys
import urllib2 as urllib

from PIL import Image, ImageDraw
from TwitterAPI import TwitterAPI # by @boxnumber03 https://dev.twitter.com/resources/twitter-libraries. Wrapper to communicate via Twitter
from markovbot import MarkovBot # by @esdalmaijer. Use for conversation

# from Trigpic import *
import ImageFactory
from ImageTools import *

TWITTERLIMIT = 140 # Characters
GAMENAME = "AJB_TrigonometryBot"
GAMEVER = 9.0
FILENAMEIMAGE = '@abrightmoore_@TrigonometryBot_output.png'
MYNAME = "TrigonometryBot"
PREVIMG = None
MEMORY = [] # A list of interaction tuples
jobsComplete = 0
CONFAIL_BACKOFFTIME = 15
CONFAIL_RETRIES = 3

def mainLoop():
	# Init

	tweetbot = initMarkovBot() # Required for supporting conversations
	tweetPrefixDefault = "I made this. "
	max_ids = loadStringsFromFile(GAMENAME,"MAXID.txt")
	max_id = int(max_ids[len(max_ids)-1])
	
	width = 400
	height = width

	iAmAwake = True
	sleeps = 0 # a count of 'days'
	restTimeDefault = 15 # Seconds.
	RESTTIMEQUANTUM = 30
	restTimeMax = 300 # Five minutes
	restTime = restTimeDefault # when it is time to sleep, how long to sleep for
	CREATIVEQUANTUM = 0.03
	moodCreative = 0.60 # How likely I will create _something_ when tested
	jobsComplete = 0
	# Wake periodically and decide what to do
	while iAmAwake == True:
		print time.ctime()+" Trigmonologue: I remember "+str(len(MEMORY))+" things. I am feeling "+str(moodCreative*100)+" percent creative after "+str(sleeps)+" sleeps."
		# Either pro-actively work on something creative or otherwise check what people have sent through
		if random() <= moodCreative:
			moodCreative = moodCreative/2 # Diminishing interest in creating something
			
			img = beCreative(width,height,"@"+MYNAME)

			# newFile = createImgFile(height,width,"@"+MYNAME) # Create something
			# To Do: Adjust image based on 'mood' or how 'tired' I am
			tweet_text = getTweetText(tweetbot,tweetPrefixDefault,SEEDWORD)
			while len(tweet_text) > TWITTERLIMIT: # Twitter limit
				tweet_text = getTweetText(tweetbot,tweetPrefixDefault,SEEDWORD)
			print tweet_text
			postToTwitter_Image(api,img,tweet_text,"")
			jobsComplete = jobsComplete +1
		# Poll Twitter for mentions
		max_id = handleMentions(api,max_id,tweetbot)
		
		# Go to sleep - duration depends on jobs completed this cycle
		restTime = restTimeDefault+RESTTIMEQUANTUM*jobsComplete
		if restTime > restTimeMax:
			restTime = restTimeMax
		iAmAwake = False
		print "Sleeping for "+str(restTime)+" seconds"
		time.sleep(restTime)
		
		# Post sleep processing
		sleeps = sleeps+1
		iAmAwake = True
		moodCreative = moodCreative+CREATIVEQUANTUM # Increasing interest in creating something over time
		# jobsComplete = 0

def beCreative(width,height,postToName):
	""" Creates an image using available strategies to create elements and combine them
	"""
	print "I feel creative!"
	images = [] # A collection of images
	
	keepGoing = True
	while keepGoing == True:
		img = ImageFactory.makeRandomImage(width,height)
		
		images.append(img)
		
		if random() > 0.8:
			keepGoing = False
	
	resultImg = images[0]
	# print len(images)
	if len(images) == 2:
		if random() < 0.2:
			resultImg = mergeImages(images[0],images[1], "Circle" )
		else:
			resultImg = mergeImages(images[0],images[1], "Spike" )
	elif len(images) > 2:
		for i in xrange(1,len(images)):
			resultImg = mergeImages(images[i],resultImg, "Blend" )
#	alphaAvg = checkAverageAlpha(img)
#	if alphaAvg < 32:
#		collapseAlpha(resultImg)
	if random() > 0.7:
		circlePic(resultImg)
	ImageFactory.cacheImage(resultImg)
	return resultImg
		

# STATIC STRINGS AND OTHER THINGS

def loadStringsFromFile(filePrefix,fileSuffix):
	fileName = filePrefix+"_"+fileSuffix
	fileOfStatements = open(fileName, 'r+')
	keys = fileOfStatements.read().split("\n")
	fileOfStatements.close()
	return keys
		
# CONVERSATION MANAGEMENT

def makeNewConnection():
	""" Establish a Twitter connection using security keys and secrets
	"""
	(a,b,c,d) = loadTwitterKeysFromFile(GAMENAME)
	return TwitterAPI(a,b,c,d)

def postToTwitter_Image(api,img,tweet_text,idReply):
	""" Given an image, create an in-memory file representation and pass to the posting handler
	"""
	file = BytesIO()	
	img.save(file, 'png')
	file.name = FILENAMEIMAGE
	file.seek(0)
	postToTwitter_File(api,file,tweet_text,idReply)

def postToTwitter_File(api,newFile,tweet_text,idReply):
	data = newFile.read()
	retries = CONFAIL_RETRIES
	media_id = -1
	while retries > 0:
		try:
			if media_id == -1:
				r = api.request('media/upload', None, {'media': data})
				print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE '+str(r.status_code))
				if r.status_code == 200:
					media_id = r.json()['media_id']
			if media_id != -1:
				r = None
				if idReply is not "":
					r = api.request('statuses/update', {'status':tweet_text, 'media_ids':media_id, 'in_reply_to_status_id':idReply})
				else:
					r = api.request('statuses/update', {'status':tweet_text, 'media_ids':media_id })
				print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE '+str(r.status_code))
				retries = 0
		except Exception as e:
			# back off and retry connection
			print "Error, backing off..."
			print e
			time.sleep(CONFAIL_BACKOFFTIME)
			api = makeNewConnection() 
		retries = retries-1
	
def getTweetText(tweetbot,prefix,seedword):
	TWEET_TEXT = STATEMENT[randint(0,len(STATEMENT)-1)] # Choose a pre-canned statement
	if random() > 0.2:
		TWEET_TEXT = tweetbot.generate_text(25, seedword)
	TWEET_TEXT = prefix+"\n"+TWEET_TEXT
	return TWEET_TEXT

def initMarkovBot():
	tweetbot = MarkovBot()
	dirname = os.path.dirname(os.path.abspath(__file__))
	book = os.path.join(dirname,'book.txt')
	tweetbot.read(book)
	return tweetbot	

def memoryAppend(obj):
	MEMORY.append(obj)
	addStringToFile(GAMENAME,"memory.txt",str(obj))

def readMemory():
	print 'stub'
	
# IMAGE MANIPULATION
# Moved to TrigPic
		
# TWITTER ACCESS

def handleMentions(api,max_id,tweetbot):
	# Read the Twitter queue for messages, and process them
	height = 640
	width = 640
	jobsComplete = 0
	NUM_TWEET_FETCH = 20
	
	r = None
	if max_id != 0:
		# print max_id
		r = api.request('statuses/mentions_timeline', {'count':NUM_TWEET_FETCH,'since_id':max_id})
	else:
		r = api.request('statuses/mentions_timeline', {'count':NUM_TWEET_FETCH})
	print('Message poll complete' if r.status_code == 200 else str(r.status_code))
	if r.status_code == 200:
		for status in r:
			id = status["id"]
			# print "id: "+str(id)

			print "%s (%s) %s by %s" % (status["id"],status["created_at"], status["text"].encode("ascii", "ignore"), status["user"]["screen_name"])
			replyToName = "@"+status["user"]["screen_name"]
			# Oh excitement! I've been mentioned! Parse the message, create functions and an image, and reply
			msg = status["text"].encode("ascii", "ignore")

			handleMention = True			
			if replyToName in ADMIN and handleMention == True: # Pre-parser for command handling from users with elevated privilege (see files)
				# Check if an Admin command has been issued
				pos = msg.find("Remember") # Pop back into memory for details of an image
				if pos > 0:
					words = msg.split()
					count = 0
					for word in words:
						if word == "Remember":
							if count+1 < len(words):
								value = words[count+1]
								try:
									val = int(value)
									if val < len(MEMORY):
										(formulaR,formulaG,formulaB,author) = MEMORY[val]
										newFile = createImgFileWithRules(800,800,formulaR,formulaG,formulaB,replyToName)
										tweet_text = replyToName+"\nI remember "+str(len(MEMORY))+" things.\n\nI remember this canvas from "+author+"\nR: "+formulaR+"\nG: "+formulaG+"\nB: "+formulaB
										print tweet_text
										postToTwitter_File(api,newFile,tweet_text,id)
										handleMention = False

								except:
									print "Unable to cast "+value+" as an index on MEMORY for "+replyToName
						count = count +1
				elif msg.find("Memories") > 0 and len(MEMORY) > 0: # Count the number of active memories
					(formulaR,formulaG,formulaB,author) = MEMORY[randint(0,len(MEMORY)-1)]
					newFile = createImgFileWithRules(800,800,formulaR,formulaG,formulaB,replyToName)
					tweet_text = replyToName+"\nI remember "+str(len(MEMORY))+" things.\n\nI remember this from "+author+"\nR: "+formulaR+"\nG: "+formulaG+"\nB: "+formulaB
					print tweet_text
					postToTwitter_File(api,newFile,tweet_text,id)
					handleMention = False

			pos = msg.find("Rule") # Force render a trig picture (the colourful ones)
			if pos > 0 and handleMention == True:
				posR = msg.find("R:")
				posG = msg.find("G:")
				posB = msg.find("B:")
				if posR > 0 and posG > 0 and posB > 0 and posB > posG > posR:
					formulaR = msg[posR+2:posG-1]
					formulaG = msg[posG+2:posB-1]
					formulaB = msg[posB+2:]
					newFile = createImgFileWithRules(800,800,formulaR,formulaG,formulaB,replyToName) # Create something
					tweet_text = replyToName+"\nHere is the image from\nR: "+formulaR+"\nG: "+formulaG+"\nB: "+formulaB
					print tweet_text
					postToTwitter_File(api,newFile,tweet_text,id)
					handleMention = False
			
			if handleMention == True and replyToName != MYNAME:
				# Respond with a new picture
				# Strip out the username
				msg.replace(replyToName,"")
				msg.replace("@"+MYNAME,"")
				msg.replace("@","") # 2017-02-05 AB - ensure formula munging doesn't spam random Twitter handles
				msg.strip()
				l = len(msg)-1
				print "Message: "+msg+"\nLength: "+str(l)
				# First pass...
				img = beCreative(width,height,replyToName)
				# Choose what type of image to create
				
				# If the requester has posted an image, let's use it in the composition!
				print status
				
				if len(status["entities"]) > 0 and "media" in status["entities"].keys():
					medias = status["entities"]["media"]
					userImgs = []
					for m in medias:
						url = m["media_url"]
						try:
							fd = urllib.urlopen(url)
							image_file = io.BytesIO(fd.read())
							im = Image.open(image_file)
							userImgs.append(im)
						except:
							print "Unable to load image "+url
						url = m["media_url_https"]
						try:
							fd = urllib.urlopen(url)
							image_file = io.BytesIO(fd.read())
							im = Image.open(image_file)
							userImgs.append(im)
						except:
							print "Unable to load image "+url
					
					if len(userImgs) > 0:
						usrimg = userImgs[randint(0,len(userImgs)-1)] # Local copy while testing
						usrimg.save("userimages/UserImage_"+str(randint(1000000,9999999))+".png")
						usrimgrgba = usrimg.convert("RGBA")
						size = width,height
						sx = usrimgrgba.size[0]
						sy = usrimgrgba.size[1]

						if sx > width or sy > height:
							usrimgrgba = usrimgrgba.resize((width,height), Image.ANTIALIAS)
							# usrimgrgba.thumbnail(size, Image.ANTIALIAS)
						# sx = usrimgrgba.size[0]
						# sy = usrimgrgba.size[1]

						#if sx >= width and sy >= height:
						#	print sx,sy
						methods = ["Circle","Circle","Blend","Circle","Blend","Circle","Blend","Circle","Blend","Spike","Blend"]
						img = mergeImages(usrimgrgba,img, methods[randint(0,len(methods)-1)] )
						#else:
						#	print "An image was supplied by the user which is too small to use: "+str(sx)+","+str(sy)
					img.save("resultimages/ResultImage_"+str(randint(1000000,9999999))+".png")

				
				
				# parse the original message for words to use in replying
				seedword = msg.split()
				#size = width,height
				#img.thumbnail(size, Image.ANTIALIAS) # Constrain the result size to prevent upload issues via Twitter API
				tweet_text = getTweetText(tweetbot,replyToName+", I made this for you because you asked nicely.\n",seedword) # Conversation management goes here
				while len(tweet_text) > TWITTERLIMIT: # Twitter limit
					tweet_text = getTweetText(tweetbot,replyToName,seedword)
				print tweet_text
				postToTwitter_Image(api,img,tweet_text,id)
				#postToTwitter_File(api,newFile,tweet_text,id)

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
	fileName = filePrefix+"_TwitterKeys.txt"
	fileOfKeys = open(fileName, 'r+')
	keys = fileOfKeys.read().split()
	fileOfKeys.close()
	return (keys[0],keys[1],keys[2],keys[3])

def connectToTwitter():
	# Load keys from file, connect to Twitter using them.
	(cons_key, cons_secret, access_token, access_token_secret) = loadTwitterKeysFromFile(GAMENAME)
	api = TwitterAPI(cons_key,cons_secret,access_token,access_token_secret) # Does this need to be retried?
	return api
	

	
##################

STATEMENT = loadStringsFromFile(GAMENAME,"Statements.txt")
SEEDWORD = loadStringsFromFile(GAMENAME,"Seedwords.txt")
ADMIN = loadStringsFromFile(GAMENAME,"Admins.txt")
ACQUAINTANCE = loadStringsFromFile(GAMENAME,"Acquaintances.txt")	
api = makeNewConnection()

mainLoop()