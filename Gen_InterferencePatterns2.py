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

from ImageTools import *
from Gen_Trigonometry import calcFormula

def draw(img):
	ifxPatterns2(img)

def ifxPatterns2(img):
	# CONSTANTS
	method = "IFXPatterns2"
	print '%s: Started at %s' % (method, time.ctime())
	width = img.size[0]
	depth = img.size[1]
	
	# Now we have a list of plots to use to place things on. We need to understand the city zoning rules.
	zonePoints = []
	boxW = width
	boxD = depth
	# High-rise
	zonePoints.append((0.1,boxW>>1,boxD>>1,boxW,0)) # Power, x pos, z pos, wavelength, phase shift
	# Residential
	#zonePoints.append((0.5,randint(0,boxW>>1),randint(0,boxW>>1),boxW,pi)) # Power, x pos, z pos, wavelength
	for i in xrange(0,randint(1,10)):
		zonePoints.append((0.1,randint(0,boxW),randint(0,boxW),boxW,pi)) # Power, x pos, z pos, wavelength

	# Debug - plot out the zoning pattern
	#img = pygame.Surface((boxW,boxD))
	#px = pygame.surfarray.pixels3d(img)
	pix = img.load()
	for x in xrange(0,boxW):
		for z in xrange(0,boxD):
			valHere = 0
			count = 0
			for (amp,ppx,ppz,wavelength,offset) in zonePoints:
				dx = x-(ppx)
				dz = z-(ppz)
				dist = sqrt(dx**2+dz**2)
				ratio = dist/wavelength
				contribution = cos(offset+ratio*pi*2.0)
				valHere += valHere+contribution
				count += 1
			valHere = (valHere+1.0)/2.0 * 255
			lowerBound = 0
			excess = 0
			if valHere < 0: 
				lowerBound = 0-valHere
				valHere = 0
			if valHere > 255:
				excess = valHere - 255
				valHere = 255
			(R,G,B,A) = pix[x,z]
			R = int(lowerBound)+R
			G = int(excess)+G
			B = int(valHere)+B
			pix[x,z] = (R>>1,G>>1,B>>1)
	# del pix
#	pygame.image.save(img,"PROCGEN_City_ZONE_"+str(randint(1000000000,9999999999))+".png")
	print '%s: Ended at %s' % (method, time.ctime())
