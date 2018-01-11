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
		return result

	def getNext(self):
		total = sum(self.nextWords.values())
		choice = randint(0,total-1)
		value = 0
		for key in self.nextWords.keys():
			v = self.nextWords.get(key)
			value += v
			if value >= choice:
				result = key
				break
		return result

def validWord(word):
	return (word.isalpha() or word == '.')

def getWordChain():
	fileNames = None
	with open('LanguageExampleFiles.txt','r') as myfiles:
		data = myfiles.read()
		fileNames = string.split(data)
		
	words = {}

	for fileName in fileNames:
		lastWord = None

		data = string.split(open(fileName).read())
		# re.findall(r'\w+', open(fileName).read())
		if DEBUG: print data

		for word in data:
			word = word.lower()
			if validWord(word):
				if lastWord in words:
					prevWord = words.get(lastWord)
					prevWord.add(word)
					if word in string.punctuation:
						prevWord.end = True
					if lastWord in string.punctuation:
						prevWord.start = True
				if word in words:
					theWord = words.get(word)
					theWord.count += 1
				else:
					newWord = Word(word)
					newWord.start = True
					words[word] = newWord
					
				lastWord = word

	if DEBUG:
		print "Parsed files. Result:"
		for key in words:
			print words[key].label,words[key].count,": ", words[key]

	# Clean up - simple grammar rules
	
	removeWordLinks(words,"the","a")
	removeWordLinks(words,"a","but")
	removeWordLinks(words,"a","a")
	removeWordLinks(words,"to","the")
			
	return words

def removeWordLinks(words,word,wordToRemove):
	theWord = words.get(word)
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
			keepTrying = False
	
	theWordsUsed = []
	result = theWord.label.title()
	#print "START: "+result
	keepGoing = True
	count = 15
	while keepGoing:
		theWordsUsed.append(theWord)
		nextWord = theWord.getNext()
		if nextWord == "i":
			result = result+" I"
		else:
			result = result+" "+nextWord
		theWord = words.get(nextWord)
		count -= 1
		#print nextWord
#		if nextWord.lower() in CONJUNCTIONS:
#			keepGoing = True
		if theWord.end == True and theWord.label.lower() not in CONJUNCTIONS and (nextWord in string.punctuation or count < 1):
			keepGoing = False
		if keepGoing == False and nextWord not in string.punctuation:
			result = result + '.'
			
	if False:
		print "Words used:"
		for word in theWordsUsed:
			print word
	return result
			
#words = getWordChain()
#print makeSentence(words,20)