# @TheWorldFoundry

import sys
import string
from collections import Counter
import re
from random import choice,randint,random

DEBUG = False

class Word:
	def __init__(self, label):
		self.label = label.lower()
		self.count = 1
		self.nextWords = Counter()
		self.start = False
		self.end = False

	def add(self,newWord):
		self.nextWords[newWord] += 1

	def remove(self,word):
		self.nextWords[word] = 0
		
	def __repr__(self):
		return "Word"

	def __str__(self):
		result = "Word(\""+self.label+"\"):\n"
		for word in self.nextWords:
			count = self.nextWords.get(word)
			result = result+word+":"+str(count)+"\n"
		if self.start:
                        result = result+"\nCan start a sentence."
                if self.end:
                        result = result+"\nCan end a sentence."
		return result

	def getNext(self):
		total = sum(self.nextWords.values())
                result = None

		if total > 0:
                        choice = randint(0,total-1)+1
                        value = 0
                        for key in self.nextWords.keys():
                                v = self.nextWords.get(key)
                                value += v
                                if value >= choice:
                                        result = key
                                        break
#		print "Result is ",result
		return result

def validWord(word):
	return (word.isalpha() or word == '.' or word == ',' or len(string.split(word,".")) > 0)

def getWordChain():
        SENTENCEEND = ".?!…"
	fileNames = None
	with open('LanguageExampleFiles.txt','r') as myfiles:
		data = myfiles.read()
		fileNames = string.split(data)
		
	words = {}

	for fileName in fileNames:
		lastWord = None
                theFile = open(fileName).read()
                for c in string.punctuation:
                        replaceString = ' '+c+' '
                        theFile = string.replace(theFile, c,replaceString)
                if DEBUG: print theFile
                
		data = string.split(theFile)
		# re.findall(r'\w+', open(fileName).read())
		if DEBUG: print data

		for word in data:
                        if DEBUG: print "Processing ",word
			word = word.lower()
			if validWord(word):
				if lastWord in words:
                                        if DEBUG: print lastWord," is in words"
					prevWord = words.get(lastWord)
					prevWord.add(word)
					if word in SENTENCEEND:
						prevWord.end = True
					if lastWord in SENTENCEEND:
						prevWord.start = True
				if word in words:
					theWord = words.get(word)
					theWord.count += 1
				else:
					newWord = Word(word)
                                        if lastWord is not None and lastWord in SENTENCEEND:
        					newWord.start = True
					words[word] = newWord
					if DEBUG: print "Added ",newWord
				lastWord = word

	if DEBUG:
		print "Parsed files. Result:"
		for key in words:
			print words[key].label,words[key].count,": ", words[key]

	# Clean up - simple grammar rules
	
	removeWordLinks(words,"the","a")
	removeWordLinks(words,"a","but")
	removeWordLinks(words,"a","a")
	removeWordLinks(words,"a","the")
        removeWordLinks(words,"an","but")
	removeWordLinks(words,"to","the")
	removeWordLinks(words,"they","the")
        removeWordLinks(words,"my","and")

	
			
	return words

def removeWordLinks(words,word,wordToRemove):
	theWord = words.get(word)
	if theWord is not None:
        	theWord.remove(wordToRemove)
	# pass
	
	
def makeSentence(words,count):
	CONJUNCTIONS = ["is","but","for","or","nor","so","yet","its","the","a","an","her","his","their","our","of","these","in","what","to","and","are","do","this","my","your","we","hear","be","which","resultant","each","when","where","why","who","how","had","that","with"]

	keepTrying = True
	counter = 1000
	theWord = None
	while keepTrying == True and counter > 0:
		counter -= 1
		theWord = words.get(choice(words.keys()))
		if theWord.start == True:
                        # print "Starting at ",theWord
			keepTrying = False
	
	theWordsUsed = []
	result = theWord.label.title()
	#print "START: "+result
	keepGoing = True
	count = 15
	while keepGoing:
		theWordsUsed.append(theWord)
		nextWord = theWord.getNext()
		if nextWord is not None:
                        if nextWord == "i":
                                result = result+" I"
                        elif nextWord in string.punctuation:
                                result = result+nextWord
                        else:
                                result = result+" "+nextWord
                        theWord = words.get(nextWord)
                        count -= 1
                        #print nextWord
        #		if nextWord.lower() in CONJUNCTIONS:
        #			keepGoing = True
                        if theWord.end == True and theWord.label.lower() not in CONJUNCTIONS and (nextWord in string.punctuation or count < 1):
                                keepGoing = False
                        if count < -100:
                                keepGoing = False
                        if keepGoing == False and nextWord not in string.punctuation:
                                result = result + '.'
                else:
                        keepGoing = False
	if False:
		print "Words used:"
		for word in theWordsUsed:
			print word
	return result

#result = ""
#for i in xrange(0,randint(1,40)):			
#        result = result + " " + makeSentence(getWordChain(),50)
#print result
