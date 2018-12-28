# @abrightmoore
# from numpy import *
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
import os
import time
from random import randint, random, Random
import io
from io import BytesIO
import sys
from numpy import *

from PIL import Image, ImageDraw

from Colours import *
from ImageTools import *
from Gen_Trigonometry import calcFormula

def draw(img):
	sandscape1(img)

def sandscape1(img):
	# CONSTANTS
	method = "sandscape1"
	print '%s: Started at %s' % (method, time.ctime())
	width = img.size[0]
	depth = img.size[1]
	
	# Colours
	C = []
	chance = randint(1,depth>>4)
	if chance == 1:
		C = getRandomAnalogousColours()
	elif chance == 2:
		C = getRandomComplementaryColours()
	else:
		C = getColoursBrownian(randint(16,64),randint(4,16))
	
	SMOOTHAMOUNT = 5 # randint(2,5)
	
	# Lines
	LINEHEIGHTMIN = 8
	LINEHEIGHTMAX = depth>>3
	
	pix = img.load()

	
	final = False
	lineHeight = LINEHEIGHTMAX
	counter = 0
	while lineHeight < depth:
		print "Sandscape height render",lineHeight
		# Plot a smooth curve, and colour in beneath it until we hit a non-background colour
		P = []
		P.append((0,lineHeight,0))
		P.append((0,lineHeight,0))
	
		# Add a couple of wobbles along the length
		numWobbles = randint(2,5)
		for i in xrange(1,numWobbles):
			P.append((width/numWobbles*i,lineHeight+randint(-lineHeight>>1,lineHeight>>1),0)) # Vertical wobble
	
		P.append((width-1,lineHeight,0))
		P.append((width-1,lineHeight,0))
	
		# Now... plot this line and the area beneath it
		thisColour = C[counter%len(C)]
		
		
		# And move the dial a little bit
		lineHeight += randint(LINEHEIGHTMIN,LINEHEIGHTMAX)
#		if lineHeight > depth-1 and final == False: # Make sure the top most band is tried
#			final == True
#			lineHeight = depth-1
		counter = counter+1
		
		R,G,B = thisColour
		Q = calcLinesSmooth(SMOOTHAMOUNT,P) # All the points in the smooth line
		for (x,y,z) in Q:
			py = y
			if py >= depth:
				py = depth-1
			keepGoing = True
			while keepGoing:
				if py >= 0 and py < depth:
					R1,G1,B1,A1 = pix[x,py]
					if (R1 == 0) and (G1 == 0) and (B1 == 0):
						pix[x,py] = (R,G,B)
					else:
						keepGoing = False
					py -= 1
				else:
					keepGoing = False
		
	# Finish up the last band
	for x in xrange(0,width):
		py = depth-1
		keepGoing = True
		while keepGoing:
			if py >= 0 and py < depth:
				R1,G1,B1,A1 = pix[x,py]
				if (R1 == 0) and (G1 == 0) and (B1 == 0):
					pix[x,py] = (R,G,B)
				else:
					keepGoing = False
				py -= 1
			else:
				keepGoing = False		
		py -= 1

	#img.transpose(Image.FLIP_TOP_BOTTOM)
	for x in xrange(0,width):
		for y in xrange(0,depth>>1):
			col = pix[x,y]
			col1 = pix[x,depth-1-y]
			pix[x,y] = col1
			pix[x,depth-1-y] = col
	print "Rotated"

	print '%s: Ended at %s' % (method, time.ctime())

