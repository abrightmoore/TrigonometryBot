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
        numPoints = randint(17,80)
        theRange = (width+height) ** 2
        
        for i in xrange(0,numPoints):
                scale = randint(8,1280)
                P.append((random()*pi*2.0,randint(0,theRange),0.2+random(),0.2+random()*scale))
                if random() < 0.2:
                        P.append((random()*pi*2.0,randint(0,width>>2),random(),random()*scale)) 

        # render the image
	pixels = img.load()

	for x in xrange(0,width):
		for y in xrange(0,height):
			contribution = 0.0
			count = 0
			for (ang,dist,amp,wavelength) in P:
				count += 1
				ox = dist*cos(ang)
				oy = dist*sin(ang)
				dx = ox - x
				dy = oy - y
				d = sqrt(dx**2+dy**2)
				contribution = contribution + amp*cos(d/wavelength)

			r = 0
			g = 0
			b = 0
			if count%3 == 0:
				r = 0.5+cos(contribution)/2.0
			if count%3 == 1:
				g = 1.0-contribution
			if count%3 == 2:
				b = sin(contribution*contribution) #/2.0
			contribution = abs(contribution) #/2.0)
			
			(r1,g1,b1) = (g*b/(r+1.5)+b,tan(r)-g,g+tan(g)*b)
			#print r1,g1,b1
			r1 = r1*255
			g1 = g1*255
			b1 = b1*255
			if r1 > 255:
				r1 = 255
			if r1 < 0:
				r1 = 0
			if g1 > 255:
				g1 = 255
			if g1 < 0:
				g1 = 0
			if b1 > 255:
				b1 = 255
			if b1 < 0:
				b1 = 0
			
			(r2,g2,b2,a) = pixels[x,y]
			
			# Randomise!
			if random() > 0.5:
				t = r1
				r1 = g1
				g1 = t
			if random() > 0.5:
				t = g1
				g1 = b1
				b1 = t			
			if random() > 0.5:
				t = g1
				g1 = b1
				b1 = t	
			if random() > 0.5:
				t = b1
				b1 = r1
				r1 = g1
				g1 = t

				
			# print r1,g1,b1,r2,g2,b2,a
			pixels[x,y] = ((int(r1)+r2)>>1,(int(g1)+g2)>>1,(int(b1)+b2)>>1,a)
			#print pixels[x,y]