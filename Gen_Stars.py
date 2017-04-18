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
	width = img.size[0]
	height = img.size[1]
	border = 15
	colour = (randint(0,192),randint(0,192),randint(128,255),255)
	for i in xrange(0,randint(10,100)):
		r = randint(int(border/8),border)
		x = randint(4*r+1,width-4*r-1)
		y = randint(4*r+1,height-4*r-1)
		star(img,colour,r,x,y)
		if random() > 0.3 and r < border/2:
			bubble(img,colour,int(2*r),x,y)


			
def star(img,colour,radius,x,y):
	width = img.size[0]
	height = img.size[1]
	exposureCol = (255,255,255,255)
	# Given a colour, create a sinusoidal circle of radius r at x,y where the colour tapers off and blends
	(r2,g2,b2,a2) = colour
	pix = img.load()
	radius2 = radius**2
	d = 4*radius
	for dx in xrange(-d,d+1):
		(r,g,b,a) = colour
		intensity = 1.0-abs(float(dx)/float(d))
		(r1,g1,b1,a1) = pix[x+dx,y]
		r = intensity*r+(1.0-intensity)*r1
		g = intensity*g+(1.0-intensity)*g1
		b = intensity*b+(1.0-intensity)*b1
		
		pix[x+dx,y] = (int(r),int(g),int(b),255)
	for dy in xrange(-d,d+1):
		(r,g,b,a) = colour
		intensity = 1.0-abs(float(dy)/float(d))
		(r1,g1,b1,a1) = pix[x,y+dy]
		r = intensity*r+(1.0-intensity)*r1
		g = intensity*g+(1.0-intensity)*g1
		b = intensity*b+(1.0-intensity)*b1
		pix[x,y+dy] = (int(r),int(g),int(b),255)
	for dx in xrange(-radius,radius+1):
		for dy in xrange(-radius,radius+1):
			(r1,g1,b1,a1) = pix[x+dx,y+dy]
			dist2 = dx**2+dy**2
			if dist2 < radius2/8:
				pix[x+dx,y+dy] = exposureCol
			elif dist2 <= radius2:
				dr = cos(abs(float(dist2)/float(radius2)*pi/2))
			#	print dr
				idr = 1.0-dr
				r = idr*r1+dr*r2
				g = idr*g1+dr*g2
				b = idr*b1+dr*b2
				# print(r,g,b)
				colouresult = (int(r),int(g),int(b),255)
				pix[x+dx,y+dy] = colouresult
				#print dx,dy,dist2,colouresult
	


	# Add flares?		
	
def bubble(img,colour,radius,x,y):
	width = img.size[0]
	height = img.size[1]
	
	# Given a colour, create a sinusoidal circle of radius r at x,y where the colour tapers off and blends
	(r2,g2,b2,a2) = colour
	pix = img.load()
	radius2 = radius**2
	for dx in xrange(-radius,radius+1):
		for dy in xrange(-radius,radius+1):
			(r1,g1,b1,a1) = pix[x+dx,y+dy]
			dist2 = dx**2+dy**2
			if dist2 <= radius2:
				dr = cos(abs(float(dist2)/float(radius2)*pi/2))
			#	print dr
				idr = 1.0-dr
				r = dr*r1+idr*r2
				g = dr*g1+idr*g2
				b = dr*b1+idr*b2
				# print(r,g,b)
				colouresult = (int(r),int(g),int(b),255)
				pix[x+dx,y+dy] = colouresult
				#print dx,dy,dist2,colouresult
	
	# Add flares?