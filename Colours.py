from random import *
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2

from Rotation import RotatePoint,UnRotatePoint

def getComplementaryColours(quantity):
	COLMASK = 0xff
	result = []

#       COLBASE = 0.3
	# 0.3 so we don't make it too dark nor light
#       r = (COLBASE+random()/2)*256 # x
#       g = (COLBASE+random()/2)*256 # y
#       b = (COLBASE+random()/2)*256 # z

	r = randint(32,255)
	g = randint(32,255)
	b = randint(32,255)

	result.append((r,g,b))

	# This gives a colour in the RGB colour cube. Find out what angles these are
	disth2 = r**2+g**2
	theta = atan2(r,g)
	phi = atan2(b,sqrt(disth2))
	# - to find the other two colours, we need to rotate this point around the line from 0,0,0 to 1,1,1 by the right number of degrees and read off the coordinates
	angleRot = pi*2.0/float(quantity)
	# rotate up 45 degrees and back 45 degrees
	angleDelta = pi/4

	(x,y,z) = RotatePoint((r,g,b), (0,0,0), -angleDelta, angleDelta) # Shift the axis to normalise space along r=g=b line
#       print (x,y,z)

	for i in xrange(1,quantity):
		(r1,g1,b1) = RotatePoint((x,y,z), (0,0,0), -angleDelta*i, 0) # find each rotation in normalised space
		result.append(UnRotatePoint((r1,g1,b1),(0,0,0),-angleDelta,angleDelta)) # Map back to the colour cube

	resultConstrained = []
	for (r,g,b) in result:
#               if r > 255 or g > 255 or b > 255:
#                       print r,g,b
		if r > 255:
			r = 255
		if g > 255:
			g = 255
		if b > 255:
			b = 255
		if r < 0:
			r = 0
		if g < 0:
			g = 0
		if b < 0:
			b = 0
		resultConstrained.append((int(r)&COLMASK,int(g)&COLMASK,int(b)&COLMASK))

	return resultConstrained
	
def getRandomComplementaryColours():
	return getComplementaryColours(randint(2,64))

def getRandomAnalogousColours():
	C = getComplementaryColours(12)
	R = []
	for i in xrange(0,2):
		R.append(C[i])
	return R
	
def getColoursBrownian(quantity,delta):
	result = []
	
	r = randint(64,255)
	g = randint(64,255)
	b = randint(64,255)
	
	for i in xrange(0,quantity):
		result.append((r,g,b))
		# Calc a new value
		r = r+randint(-1,1)*delta
		g = g+randint(-1,1)*delta
		b = b+randint(-1,1)*delta
		if r > 255:
			r = r-delta>>1
		if r < 0:
			r = r+delta>>1
		if g > 255:
			g = g-delta>>1
		if g < 0:
			g = g+delta>>1
		if b > 255:
			b = b-delta>>1
		if b < 0:
			b = b+delta>>1
			
	return result