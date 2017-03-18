# @abrightmoore

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
import os
import time
from random import randint, random, Random
import io
from io import BytesIO
import sys


from PIL import Image, ImageDraw

from Colours import *

def draw(img):
	makeInterferenceImage(img)
	return img
	
def makeInterferenceImage(img):
	width = img.size[0]
	height = img.size[1]
	P = []
        numPoints = randint(1,17)
        theRange = (width+height) ** 2
        
        for i in xrange(0,numPoints):
                scale = randint(8,1280)
                P.append((random()*pi*2.0,randint(0,theRange),random(),random()*scale))
                if random() < 0.2:
                        P.append((random()*pi*2.0,randint(0,width>>2),random(),random()*scale)) 
#        C = getComplementaryColours(randint(3,128))
		C = []
		chance = randint(1,10)
		if chance == 1:
			C = getRandomAnalogousColours()
		elif chance == 2:
			C = getRandomComplementaryColours()
		else:
			C = getColoursBrownian(randint(16,64),randint(4,16))

        # render the image
	pixels = img.load()
	for x in xrange(0,width):
		for y in xrange(0,height):
			contribution = 0.0
			for (ang,dist,amp,wavelength) in P:
				ox = dist*cos(ang)
				oy = dist*sin(ang)
				dx = ox - x
				dy = oy - y
				d = sqrt(dx**2+dy**2)
				contribution = contribution + amp*cos(d/wavelength)
			size = contribution*float(len(C))
			#print size
			(r1,g1,b1) = C[int(abs(float(size)))%len(C)]
			(r2,g2,b2,a) = pixels[x,y]
			# print r1,g1,b1,r2,g2,b2,a
			pixels[x,y] = ((r1+r2)>>1,(g1+g2)>>1,(b1+b2)>>1,a)
			#print pixels[x,y]