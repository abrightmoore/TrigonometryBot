# @abrightmoore

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
import os
import time
from random import randint, random, Random
import io
from io import BytesIO
import sys
from numpy import *

from PIL import Image, ImageDraw
import imageio

from ImageTools import *
from Gen_Trigonometry import calcFormula
from Colours import *

def draw(img):
	caves(img)
	# img.save("dungeon/Dungeon_"+str(randint(1000000,9999999))+".png")
	
def caves(img):
	width = img.size[0]
	height = img.size[1]
	R = Random(randint(1,999999999999))
	
	# Find locations for Rooms. Work in a virtual space which we will "project" onto the canvas later
	# Use points for regions
	P = []

	numPoints = R.randint(16,32)
	theRange = (width+height) ** 2
	
	for i in xrange(0,numPoints):
		scale = randint(32,32+width)
		P.append((random()*pi*2.0,randint(theRange>>2,theRange),random(),abs(0.5+random()/2)*scale))
#		if random() < 0.2:
#			P.append((random()*pi*2.0,randint(0,width>>2),random(),random()*scale))

	max = -99999.0
	min = abs(max)
	F = zeros((width,height))
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
			size = contribution/float(len(P))
			F[x,y] = size
			if size < min:
				min = size
			if size > max:
				max = size

	# only draw the lines within the band
	(r1,g1,b1) = (255,255,255)
	linethrough = (max-min)/16 #abs(R.random()/4)*(max-min)+min
	bandwidth = 0.03
				
	print min,max,linethrough, bandwidth
	pixels = img.load()
	for x in xrange(0,width):
		for y in xrange(0,height):
			size = F[x,y]
			if size >= linethrough-bandwidth and size <= linethrough+bandwidth: #size >= linethrough-bandwidth and size <= linethrough+bandwidth: # Are we within bounds
				(r2,g2,b2,a) = pixels[x,y]
				pixels[x,y] = ((r1+r2)>>1,(g1+g2)>>1,(b1+b2)>>1,a)
	
	
	